from typing import List, Dict, Any
import re
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter 
import logging
import chromadb
from chromadb.config import Settings
from libs.ollama_embedding import OllamaEmbeddingFunction

logger = logging.getLogger(__name__)


class CaseProcessor:
    def __init__(self,host: str = "localhost", port: int =6789):
        self.client = chromadb.HttpClient(host=host,port=port)

        self.embedding_function = OllamaEmbeddingFunction("nomic-embed-text")

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap = 50,
            separators = ['\n\n','\n',' ','','. ']
        )

        self.collection = self._initialize_collection()

        if not self.validate_collection():
            logger.error("Collection validation failed - RAG may not work properly")

        self.case_types = {
    'THEFT': ['theft', 'stolen', 'robbery', 'burglary', 'larceny', 'pickpocketing', 'shoplifting', 'shoplifter', 'stealing'],
    'DRUG_TRAFFICKING': ['drug', 'narcotics', 'trafficking', 'substance abuse', 'illegal drugs', 'smuggling', 'distribution'],
    'FRAUD': ['fraud', 'scam', 'phishing', 'cheat', 'identity theft', 'embezzlement', 'counterfeit', 'deception', 'misrepresentation'],
    'GANG_ACTIVITY': ['gang', 'violence', 'street-fight', 'gang-related', 'organized crime', 'gangster', 'criminal organization'],
    'CYBERCRIME': ['cyber', 'hack', 'malware', 'virus', 'phishing', 'cyberbullying', 'data breach', 'ransomware', 'identity theft'],
    'KIDNAP': ['missing', 'kidnap', 'abduction', 'hostage', 'child abduction', 'disappearance', 'forcible confinement'],
    'HOMICIDE': ['homicide', 'murder', 'manslaughter', 'assassination', 'killing', 'death', 'murdered', 'slaying'],
    'ASSAULT': ['assault', 'battery', 'attack', 'physical violence', 'domestic violence', 'beating', 'physical harm'],
    'SEXUAL_OFFENSES': ['rape', 'sexual assault', 'molestation', 'indecent exposure', 'harassment', 'sexual harassment', 'groping'],
    'ARSON': ['arson', 'fire', 'burning', 'firebombing', 'incendiary device', 'deliberate fire'],
    'TERRORISM': ['terrorism', 'bombing', 'extremism', 'radicalization', 'terrorist attack', 'extremist', 'jihadist'],
    'VANDALISM': ['vandalism', 'graffiti', 'property damage', 'defacement', 'destruction', 'criminal mischief'],
    'PUBLIC_DISTURBANCE': ['public disturbance', 'riot', 'protest', 'unlawful assembly', 'loitering', 'disorderly conduct', 'demonstration'],
    'TRAFFICKING': ['human trafficking', 'sex trafficking', 'labor trafficking', 'exploitation', 'forced labor', 'child trafficking'],
    'BRIBERY': ['bribery', 'corruption', 'kickbacks', 'payoffs', 'illegal payment'],
    'EXTORTION': ['extortion', 'blackmail', 'coercion', 'threats', 'forced payment'],
    'WEAPONS_OFFENSE': ['illegal weapons', 'firearms', 'gun violence', 'arms trafficking', 'concealed weapons'],
    'MISSING_PERSON': ['missing person', 'runaway', 'lost', 'disappearance', 'unaccounted for', 'abducted person'],
    'ROAD_CRIMES': ['hit and run', 'reckless driving', 'drunk driving', 'traffic violation', 'vehicular manslaughter', 'road rage'],
    'SMUGGLING': ['smuggling', 'contraband', 'illegal trade', 'bootlegging', 'trafficking'],
    'ESPIONAGE': ['espionage', 'spying', 'intelligence theft', 'leaking information'],
    'HATE_CRIME': ['hate crime', 'racial violence', 'bias-motivated crime', 'hate speech', 'discrimination'],
    'FORGERY': ['forgery', 'document falsification', 'check fraud', 'signature fraud'],
    'ESCAPE': ['prison escape', 'jailbreak', 'fugitive', 'escapee', 'flight from custody'],
    'TRESPASSING': ['trespassing', 'unauthorized entry', 'illegal occupancy', 'breaking and entering'],
    'STALKING': ['stalking', 'cyberstalking', 'harassment', 'obsessive behavior', 'persistent following'],
    'ENVIRONMENTAL_CRIME': ['environmental crime', 'illegal dumping', 'pollution', 'wildlife trafficking', 'illegal fishing'],
    'VIOLATION_OF_ORDER': ['restraining order violation', 'protection order violation', 'no-contact order violation'],
    'CHILD_ABUSE': ['child abuse', 'child neglect', 'child endangerment', 'child exploitation', 'child maltreatment'],
    'ANIMAL_CRUELTY': ['animal cruelty', 'animal abuse', 'illegal poaching', 'animal neglect', 'inhumane treatment'],
    'FINANCIAL_CRIMES': ['money laundering', 'tax evasion', 'insider trading', 'financial fraud', 'embezzlement'],
    'COUNTERFEITING': ['counterfeiting', 'fake currency', 'imitation goods', 'piracy', 'counterfeit goods'],
    'HOSTAGE_SITUATION': ['hostage situation', 'barricade incident', 'hostage standoff', 'kidnapping for ransom'],
    'SLANDER_OR_LIBEL': ['defamation', 'slander', 'libel', 'character assassination', 'false accusations'],
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
                },
                embedding_function=self.embedding_function
            )
            logger.info('created new cases collection')

            initial_cases = {
            'CYBERCRIME': {
                'content': """Investigation revealed a coordinated attack on quantum banking networks by the 
                group known as BytePhantoms. Primary suspect email cypher@bytephantom.net coordinated with 
                accomplices using encrypted channels. Digital traces show connections to auxiliary accounts 
                phantom.ops@securemail.com and shadow.net@darkweb.com. The group deployed advanced malware 
                'QuantumBreaker v2.1' across multiple financial networks. Security logs identified source IPs 
                192.168.13.37 and 10.20.30.40 as primary command nodes. Cryptocurrency wallets 
                3FZbgi29cpjq2GjdwV8eyHuJJnkLtktZc5 and 8X7gh1K99pqBGjx3V1ayGuLLqkMmbt2Yc8 were used for 
                fund transfers. Communication intercepted between devices MAC:00:1B:44:11:3A:B7 and 
                MAC:00:1B:44:11:3A:B9 revealed planned attacks on additional networks.""",
                'analysis': {
                    'nodes': [
                        {
                            "id": "BytePhantoms",
                            "label": "BytePhantoms Group",
                            "type": "Organization",
                            "threat_level": "High",
                            "location": "Unknown"
                        },
                        {
                            "id": "Suspect1",
                            "label": "Primary Operator",
                            "type": "Person",
                            "email": "cypher@bytephantom.net",
                            "role": "Coordinator"
                        },
                        {
                            "id": "Suspect2",
                            "label": "Secondary Operator",
                            "type": "Person",
                            "email": "phantom.ops@securemail.com",
                            "role": "Technical Support"
                        },
                        {
                            "id": "Malware1",
                            "label": "QuantumBreaker",
                            "type": "Tool",
                            "version": "2.1",
                            "category": "Malware"
                        },
                        {
                            "id": "Node1",
                            "label": "Command Node 1",
                            "type": "Infrastructure",
                            "ip": "192.168.13.37",
                            "status": "Active"
                        },
                        {
                            "id": "Wallet1",
                            "label": "Primary Wallet",
                            "type": "Asset",
                            "address": "3FZbgi29cpjq2GjdwV8eyHuJJnkLtktZc5",
                            "currency": "Bitcoin"
                        }
                    ],
                    'edges': [
                        {"source": "Suspect1", "target": "BytePhantoms", "type": "MEMBER_OF"},
                        {"source": "Suspect2", "target": "BytePhantoms", "type": "MEMBER_OF"},
                        {"source": "BytePhantoms", "target": "Malware1", "type": "DEPLOYS"},
                        {"source": "Suspect1", "target": "Node1", "type": "CONTROLS"},
                        {"source": "BytePhantoms", "target": "Wallet1", "type": "OWNS"},
                        {"source": "Suspect1", "target": "Suspect2", "type": "COMMUNICATES_WITH"}
                    ]
                }
            },
            'THEFT': {
                'content': """Investigation into the Eclipse Syndicate vehicle theft operation identified key 
                players using burner phones +1-555-ECLIPSE and +1-555-SHADOW. Surveillance confirmed meetings 
                at coordinates 40.7829° N, 73.9654° W. Stolen vehicles include Tesla Model S (Plate: VS789X) 
                equipped with custom signal jammers, and modified Audi RS7 (Plate: HX456Y) used for transport. 
                Suspect communications monitored through email accounts eclipse.prime@anon.net and 
                shadow.tech@secure.org. CCTV footage from locations CAM_ID:VS001 through CAM_ID:VS005 shows 
                regular pattern of vehicle movements. Tracking devices serial numbers TR789456 and TR789457 
                were planted in target vehicles.""",
                'analysis': {
                    'nodes': [
                        {
                            "id": "EclipseSyndicate",
                            "label": "Eclipse Syndicate",
                            "type": "Organization",
                            "size": "15-20 members",
                            "territory": "Metropolitan"
                        },
                        {
                            "id": "Phone1",
                            "label": "Primary Contact",
                            "type": "Device",
                            "number": "+1-555-ECLIPSE",
                            "status": "Active"
                        },
                        {
                            "id": "Vehicle1",
                            "label": "Modified Tesla",
                            "type": "Asset",
                            "plate": "VS789X",
                            "modifications": "Signal Jammers"
                        },
                        {
                            "id": "Location1",
                            "label": "Primary Meeting Point",
                            "type": "Location",
                            "coordinates": "40.7829° N, 73.9654° W",
                            "frequency": "Weekly"
                        },
                        {
                            "id": "Camera1",
                            "label": "Surveillance Camera 1",
                            "type": "Device",
                            "id": "CAM_ID:VS001",
                            "status": "Active"
                        },
                        {
                            "id": "Tracker1",
                            "label": "Vehicle Tracker",
                            "type": "Device",
                            "serial": "TR789456",
                            "status": "Active"
                        }
                    ],
                    'edges': [
                        {"source": "EclipseSyndicate", "target": "Phone1", "type": "USES"},
                        {"source": "EclipseSyndicate", "target": "Vehicle1", "type": "STOLEN_BY"},
                        {"source": "EclipseSyndicate", "target": "Location1", "type": "OPERATES_FROM"},
                        {"source": "Camera1", "target": "Vehicle1", "type": "MONITORS"},
                        {"source": "Tracker1", "target": "Vehicle1", "type": "TRACKS"},
                        {"source": "Location1", "target": "Camera1", "type": "MONITORED_BY"}
                    ]
                }
            },
            'FRAUD': {
                'content': """The Quantum Financial Group fraud scheme operated through shell companies 
                registered at address 123 Shadow Street, Suite 456. Primary business account number 
                ACC:789456123 linked to multiple fraudulent transactions. Network analysis revealed email 
                chain between accounts finance@quantum-holdings.com and trades@shadow-markets.net. Company 
                registration numbers REG:QFG123456 and REG:SF789012 were found to be falsified. Investigation 
                tracked wire transfers through SWIFT codes QNTMUS33 and SHDWGB2L. Document analysis showed 
                forged certificates with serial numbers CERT:789 and CERT:790.""",
                'analysis': {
                    'nodes': [
                        {
                            "id": "QuantumGroup",
                            "label": "Quantum Financial Group",
                            "type": "Organization",
                            "registration": "REG:QFG123456",
                            "status": "Fraudulent"
                        },
                        {
                            "id": "Account1",
                            "label": "Primary Account",
                            "type": "Asset",
                            "number": "ACC:789456123",
                            "bank": "Global Bank"
                        },
                        {
                            "id": "Email1",
                            "label": "Primary Contact",
                            "type": "Communication",
                            "address": "finance@quantum-holdings.com",
                            "status": "Active"
                        },
                        {
                            "id": "Location1",
                            "label": "Registered Office",
                            "type": "Location",
                            "address": "123 Shadow Street, Suite 456",
                            "status": "Shell Location"
                        },
                        {
                            "id": "Document1",
                            "label": "Forged Certificate 1",
                            "type": "Evidence",
                            "serial": "CERT:789",
                            "status": "Fraudulent"
                        },
                        {
                            "id": "Transfer1",
                            "label": "International Transfer",
                            "type": "Transaction",
                            "swift": "QNTMUS33",
                            "status": "Suspicious"
                        }
                    ],
                    'edges': [
                        {"source": "QuantumGroup", "target": "Account1", "type": "CONTROLS"},
                        {"source": "QuantumGroup", "target": "Location1", "type": "REGISTERED_AT"},
                        {"source": "Email1", "target": "Transfer1", "type": "AUTHORIZES"},
                        {"source": "QuantumGroup", "target": "Document1", "type": "FORGED_BY"},
                        {"source": "Account1", "target": "Transfer1", "type": "SOURCE_OF"},
                        {"source": "Document1", "target": "Location1", "type": "REFERENCES"}
                    ]
                }
            }
        }

            documents = []
            metadatas= []
            ids =[]

            print(initial_cases.items())

            for idx, (case_type, case_data) in enumerate(initial_cases.items()):
                chunks = self.text_splitter.split_text(case_data['content'])
                for chunk_idx, chunk in enumerate(chunks):
                    documents.append(chunk)
                    metadatas.append({
                        'type':case_type,
                        'chunk_idx':chunk_idx,
                        'total_chunks':len(chunks),
                        'analysis':json.dumps(case_data['analysis'])
                    })
                    ids.append(f'initial_case_{idx}_chunk_{chunk_idx}')
            collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            

            return collection

    def get_similar_cases(self, case_content: List[str], case_type: str, n_results: int = 2) -> List[Dict[str, Any]]:
        try:
            # Join array into single string for splitting
            content_text = " ".join(case_content) if isinstance(case_content,list) else case_content 
            content_text=content_text.lower().strip()
            logger.debug(f"Searching for cases of type: {case_type}")
            logger.debug(f"Content text length: {len(content_text)}")
            content_chunks = self.text_splitter.split_text(content_text)
            all_results = []
            seen_contents = set()

            for chunk_idx,chunk in enumerate(content_chunks):
                test_query = self.collection.query(
    query_texts=["stolen vehicle red Honda Accord"],
    n_results=2,
    where={"type": "THEFT"}
)
                collection_data = self.collection.peek(limit=5)
                results = self.collection.query(
                    query_texts=[chunk],
                    n_results=n_results*2,
                    where={"type": case_type},
                    include=['documents','embeddings','metadatas','distances']
                )

                logger.debug(f"Content text length: {len(content_text)}")

                # Fix iteration over results
                for doc, metadata, distance in zip(
                    results.get('documents', [[]])[0],
                    results.get('metadatas', [[]])[0],
                    results.get('distances', [[]])[0]
                ):
                    try:
                        doc_key = doc[:100]
                        if doc_key in seen_contents:
                            continue
                        seen_contents.add(doc_key)
                        metadata_type = metadata.get('type','')
                        if metadata_type.upper() == case_type.upper():
                            similarity_score = 1 - distance
                            analysis = json.loads(metadata['analysis'])
                            all_results.append({
                            'type': metadata['type'],
                            'content': doc,
                            'analysis': analysis,
                            'similarity_score': similarity_score,
                            'chunk_idx': metadata.get('chunk_idx', 0),
                                'total_chunks': metadata.get('total_chunks', 1)
                        })
                    except Exception as e:
                        logger.warning(f"Error parsing similar case: {str(e)}")
                        continue

            sorted_results=sorted(
                all_results,key = lambda x:x['similarity_score'],
                reverse=True
            )

            # Fix unique results key construction
            unique_results = []
            seen_analysis=set()
            for result in sorted_results:
                # Use analysis as uniqueness criteria
                analysis_key = json.dumps(result['analysis'])
                if analysis_key not in seen_analysis:
                    seen_analysis.add(analysis_key)
                    unique_results.append(result)
                    
                    if len(unique_results) >= n_results:
                        break

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
            if isinstance(case_content, list):
                case_content = " ".join(case_content)

            chunks  = self.text_splitter.split_text(case_content)
            for idx,chk in enumerate(chunks):
                case_id = f"case_{hash(case_content)}_{idx}" 
                
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
        matches = {
    'THEFT': 0,
    'DRUG_TRAFFICKING': 0,
    'FRAUD': 0,
    'GANG_ACTIVITY': 0,
    'CYBERCRIME': 0,
    'KIDNAP': 0,
    'HOMICIDE': 0,
    'ASSAULT': 0,
    'SEXUAL_OFFENSES': 0,
    'ARSON': 0,
    'TERRORISM': 0,
    'VANDALISM': 0,
    'PUBLIC_DISTURBANCE': 0,
    'TRAFFICKING': 0,
    'BRIBERY': 0,
    'EXTORTION': 0,
    'WEAPONS_OFFENSE': 0,
    'MISSING_PERSON': 0,
    'ROAD_CRIMES': 0,
    'SMUGGLING': 0,
    'ESPIONAGE': 0,
    'HATE_CRIME': 0,
    'FORGERY': 0,
    'ESCAPE': 0,
    'TRESPASSING': 0,
    'STALKING': 0,
    'ENVIRONMENTAL_CRIME': 0,
    'VIOLATION_OF_ORDER': 0,
    'CHILD_ABUSE': 0,
    'ANIMAL_CRUELTY': 0,
    'FINANCIAL_CRIMES': 0,
    'COUNTERFEITING': 0,
    'HOSTAGE_SITUATION': 0,
    'SLANDER_OR_LIBEL': 0,
}


        
        for case_type, patterns in self.case_types.items():
            for each_line in content:
                for pattern in patterns:
                    if pattern in each_line:
                        matches[case_type]+=1
        detected_type = max(matches, key=matches.get) if matches else "OTHER"
        return detected_type
    
    def analyze_case(self,case:Dict[str,Any]) -> Dict[str,Any]:

        content = case['headline']+" "+" ".join(case['content'])

        content = [ line.lower() for line in content if len(content)!=0]
        
        case_type = self.detect_cases_types(content)

        # need to debug here
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
    
    def validate_collection(self):
        try:
            collection_info=self.collection.get()

            logger.info(f"Collection name: {self.collection.name}")

            if collection_info['ids']:
                sample_id = collection_info['ids'][0]
                logger.info(f"Sample document ID: {sample_id}")

                sample_metadata = collection_info['metadatas'][0]
                logger.info(f"Sample document metadata: {sample_metadata}")

                test_query = self.collection.query(
                        query_texts=["test query"],
                        n_results=1
                    )

                logger.info(f"Test query result structure: {test_query.keys()}")

                return True

        except Exception as e:
            logger.error(f"Collection validation failed: {e}")

            return False