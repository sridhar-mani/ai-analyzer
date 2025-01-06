from typing import List, Dict, Any
import re
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_community.embeddings import OllamaEmbeddings
import logging
import chromadb
from chromadb.config import Settings

logger = logging.getLogger(__name__)

class CaseProcessor:
    def __init__(self,host: str = "localhost", port: int =6789):
        
# initializing chromadb (embedding client)
        self.client = chromadb.HttpClient(host=host,port=port)

        self.embeddings = OllamaEmbeddings(model = "nomic-embed-text",model_kwargs={"device":'cuda'})

        self.collection = self._initialize_collection()
# text splitter for chunking large docs
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap = 50,
            separators = ['\n\n','\n',' ','','. ']
        )
        self.case_types ={
            'THEFT': ['theft', 'stolen', 'robbery', 'burglary'],
            'DRUG_TRAFFICKING': ['drug', 'narcotics', 'trafficking'],
            'FRAUD': ['fraud', 'scam', 'phishing', 'cheat'],
            'GANG_ACTIVITY': ['gang', 'violence', 'street-fight'],
            'CYBERCRIME': ['cyber', 'hack', 'malware', 'virus']
        }

    def _initialize_collection(self):
        try:
            collection = self.client.get_collection(name='cases')
            logger.info('Retrieved existing cases collection')
            return collection
        except:
            collection = self.client.create_collection(
                name="cases",
                metadata={
                    "hsnw:space":"cosine"
                }
            )
            logger.info('created new cases collection')
            # Add initial cases
            initial_cases = {
                'FRAUD': {
                    'content': """A large-scale cyber fraud network was exposed in a joint operation by the FBI and Interpol, 
                    revealing millions of dollars siphoned from unsuspecting victims worldwide.""",
                    'analysis': {
                        'type': 'FRAUD',
                        'entities': ['FBI', 'Interpol'],
                        'relationships': [
                            ('FBI', 'Interpol', 'COLLABORATED_WITH')
                        ]
                    }
                },
                'DRUG_TRAFFICKING': {
                    'content': """Police arrested members of a major drug trafficking operation spanning multiple states. 
                    The operation involved sophisticated distribution networks.""",
                    'analysis': {
                        'type': 'DRUG_TRAFFICKING',
                        'entities': ['Police', 'drug trafficking operation'],
                        'relationships': [
                            ('Police', 'drug trafficking operation', 'INVESTIGATED')
                        ]
                    }
                }
            }

            documents = []
            metadatas= []
            ids =[]

            for idx, (case_type, case_data) in enumerate(initial_cases.items()):
                documents.append(case_data['content'])
                metadatas.append({
                    'type':case_type,
                    'analysis':json.dumps(case_data['analysis'])
                })
                ids.append(f"initial_case_{idx}")

            collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            

            return collection

    def get_similar_cases(self, case_content: List[str], case_type: str, n_results: int = 2) -> List[Dict[str, Any]]:
        try:
            # Join array into single string for splitting
            content_text = " ".join(case_content)
            content_chunks = self.text_splitter.split_text(content_text)
            all_results = []

            for chunk in content_chunks:
                results = self.collection.query(
                    query_texts=[chunk],
                    n_results=n_results,
                    where={"type": case_type}
                )

                # Fix iteration over results
                for doc, metadata, distance in zip(
                    results.get('documents', [[]])[0],
                    results.get('metadatas', [[]])[0],
                    results.get('distances', [[]])[0]
                ):
                    similarity_score = 1 - distance
                    try:
                        analysis = json.loads(metadata['analysis'])
                        all_results.append({
                            'type': metadata['type'],
                            'content': doc,
                            'analysis': analysis,
                            'similarity_score': similarity_score
                        })
                    except Exception as e:
                        logger.warning(f"Error parsing similar case: {str(e)}")
                        continue

            # Fix unique results key construction
            unique_results = {}
            for result in all_results:
                result_key = f"{result['type']}_{hash(result['content'])}"
                if result_key not in unique_results or result['similarity_score'] > unique_results[result_key]['similarity_score']:
                    unique_results[result_key] = result

            return sorted(
                unique_results.values(),
                key=lambda x: x['similarity_score'],
                reverse=True
            )[:n_results]
        except Exception as e:
            logger.error(f'Error getting similar cases: {str(e)}')
            return []

    def store_successful_case(self,case_content: str,case_type: str,analysis:Dict[str,Any]):
        try:
            chunks  = self.text_splitter.split_text(case_content)
            for idx,chk in enumerate(chunks):
                case_id=f"case_{hash(case_content)(idx)}"
                
                self.collection.add(
                documents=[chk],
                    metadatas=[
                        {
                            'type':case_type,
                            'chunk_idx':idx,
                            'analysis':json.dumps(analysis),
                            'total_chunks':len(chunks)
                        }
                    ],
                    ids= [case_id]

            )
            logger.info(f"case successfully stored new case of type:{case_type}")
        except Exception as e:
            logger.error(f"Error storing case: {str(e)}")
    
    @staticmethod
    def split_into_cases(content: List[str]) -> List[Dict[str,Any]]:
        cases = []
        current_cases = []
        current_headlines = ""
        
        headline_pattern = r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?=\n|$)'

        for line in content:
            if not line.strip() and current_cases:
                    cases.append(
                        {
                            'headline': current_headlines,
                            'content':'\n'.join(current_cases)
                        }
                    )
                    current_cases=[]
                    continue
            if re.match(headline_pattern,line) and current_cases:
                cases.append(
                    {
                        'headline':current_headlines,
                        'content':'\n'.join(current_cases)
                    }
                )
                current_cases=[]
                current_headlines=line
            current_cases.append(line)
        if current_cases:
            current_cases.append(
                {
                    'headline':current_headlines,
                    'content':'\n'.join(current_cases)
                }
            )
        return cases

    def detect_cases_types(self, content:str)-> str:
        content = [ line.lower() for line in content if len(content)!=0]
        matches={
            'THEFT': 0,
            'DRUG_TRAFFICKING':0,
            'FRAUD': 0,
            'GANG_ACTIVITY': 0,
            'CYBERCRIME':0
        }
            
        
        for case_type, patterns in self.case_types.items():
            for each_line in content:
                for pattern in patterns:
                    if pattern in each_line:
                        matches[case_type]+=1
        detected_type = max(matches, key=matches.get) if matches else "OTHER"
        return detected_type
    
    def analyze_case(self,case:Dict[str,Any]) -> Dict[str,Any]:

        content = [ line.lower() for line in case['content'] if len(case['content'])!=0]
        
        case_type = self.detect_cases_types(content)

        similar_cases = self.get_similar_cases(content,case_type)

        case['similar_cases'] = similar_cases

        analysis = {
            'headline':case['headline'],
            'type': case_type,
            'similar_cases':similar_cases,
            'key_entities':[],
            'summary':""
        }

        return analysis

    def process_docuemnt(self, content: List[str]) -> List[Dict[str,Any]]:
        cases = self.split_into_cases(content)

        analyzed_cases = []

        for case in cases:
            analysis = self.analyze_case(case)
            analyzed_cases.append({
                'original':case,
                'analysis':analysis
            })
        return analyzed_cases