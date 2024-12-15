from typing import List,Dict,Any
from models.models import DocumentAnalysisResponce,EntityModel,RelationModel,AnomalyModel,GraphVizModel
import json

def create_extract_prompt(documents: List[str]) -> str:
    prompt = """You are a data extraction expert. Extract all relevant information from these documents and format it as JSON.

Follow these steps:
1. Find ALL:
   - PEOPLE (names of individuals)
   - ORGANIZATIONS (companies, agencies, groups)
   - LOCATIONS (places, addresses)
   - DATES (any time references)
   - AMOUNTS (money, quantities)

2. Identify how these entities are connected to each other

3. Look for any unusual patterns or inconsistencies

Here's an example of good extraction:
{
    "entities": [
        {"value": "John Smith", "type": "PERSON", "context": "CEO of company", "confidence": 0.9},
        {"value": "Acme Corp", "type": "ORG", "context": "Main company discussed", "confidence": 0.9},
        {"value": "New York", "type": "LOCATION", "context": "Company headquarters", "confidence": 0.9}
    ],
    "relations": [
        {"source": "John Smith", "target": "Acme Corp", "type": "WORKS_FOR", "confidence": 0.8}
    ],
    "anomalies": [
        {
            "description": "Unusual pattern found",
            "severity": "HIGH",
            "related_entities": ["entity1", "entity2"],
            "potential_impact": "Describes the possible impact"
        }
    ]
}

Documents to analyze:
"""
    for i, doc in enumerate(documents, 1):
        prompt += f"\nDocument {i}:\n{doc}\n"
    
    prompt += "\nProvide ONLY the JSON response using the exact format shown above. Include confidence scores for all entities and relations."
    
    return prompt



def parse_responce(response:Dict[str,Any])->DocumentAnalysisResponce:
    try:
        content = response['message']['content']
        data=json.loads(content)

        entities = [
            EntityModel(
                value=e['value'],
                type=e['type'],
                context=e.get('context'),
                confidence =e.get('confidence',0.5)
            ) for e in data.get('entities',[])
        ]


        relations=[
            RelationModel(
                source=r['source'],
                target=r['target'],
                  type=r['type'],
                confidence =r.get('confidence',0.5)
            ) for r in data.get('relations',[])
        ]

        anomalies=[
           AnomalyModel(
                description=a['description'],  
                severity=a.get('severity', 'MEDIUM'),
                related_entities=a.get('related_entities', []),
                potential_impact=a.get('potential_impact')
            ) for a in data.get('anomalies', [])
        ]

        nodes = []
        edges = []

        for entity in entities:
            nodes.append({
                'id':entity.value,
                'label':entity.value,
                'type':entity.type,
                'confidence':entity.confidence
            })
        for relation in relations:
            edges.append({
                'source':relation.source,
                'target':relation.target,
                'label':relation.type,
                'confidence':relation.confidence
            })

        graph_data=GraphVizModel(nodes=nodes,edges=edges)

        return DocumentAnalysisResponce(
            entities=entities,
            relations=relations,
            anomalies=anomalies,
            graph_data=graph_data
        )



    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse responce:{str(e)}")
    except KeyError as e:
        raise ValueError(f'Missing required field in responce:{str(e)}')
    
def preprocess_document(content:str)->str:
    content = " ".join(content.split())
    max_length=4000
    if len(content)>4000:
        content = content[:max_length] + '...'
    return content