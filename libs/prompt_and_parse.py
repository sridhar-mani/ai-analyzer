from typing import List, Dict, Any
import json
import re
import logging
from models.models import (
    EntityModel,
    RelationModel,
    AnomalyModel,
    GraphVizModel,
    DocumentAnalysisRequest,
    DocumentAnalysisResponse
)

logger = logging.getLogger(__name__)

def create_extract_prompt(documents: List[str]) -> str:
    prompt = """Analyze the provided text to build a comprehensive relationship network. Identify and categorize entities (persons, organizations, emails, phone numbers, locations, tools, and activities) and relationships (person-to-person, person-to-organization, activity-to-tool, communication links, etc.). Structure the response in a format suitable for Cytoscape visualization, including nodes, edges, and anomalies.

🎯 Desired Output Format
1. Entities
2. Relationships
3. Anomalies
4. Graph Data (Nodes and Edges)
5. Case Information

📋 Output Format (Example)
json
Copy code
{
  "case_info": {
    "case_number": "56789",
    "case_title": "FBI and Interpol Expose Large-Scale Cyber Fraud Network",
    "date": "2024-03-15T14:00:00Z",
    "headline": "FBI and Interpol Expose Large-Scale Cyber Fraud Network",
    "type": "Cyber Fraud Investigation",
    "page_number": 1
  },
  "entities": [
    {
      "id": "e1",
      "type": "PERSON",
      "value": "Brenda Wallace",
      "description": "62-year-old fraud victim who lost her entire savings.",
      "context": "\"I lost my entire savings because I trusted that email,\" said 62-year-old Brenda Wallace.",
      "confidence": 0.95
    },
    {
      "id": "e2",
      "type": "PERSON",
      "value": "Raj Patel",
      "description": "Victim of the fraud network who expressed frustration and called for justice.",
      "context": "Another victim, Raj Patel, remarked, \"I hope these criminals face justice.\"",
      "confidence": 0.9
    },
    {
      "id": "e3",
      "type": "ORGANIZATION",
      "value": "FBI",
      "description": "Federal Bureau of Investigation that jointly exposed the cyber fraud network.",
      "context": "A large-scale cyber fraud network was exposed in a joint operation by the FBI...",
      "confidence": 0.95
    },
    {
      "id": "e4",
      "type": "ORGANIZATION",
      "value": "Interpol",
      "description": "International police organization collaborating with the FBI to investigate fraud.",
      "context": "A large-scale cyber fraud network was exposed in a joint operation by the FBI and Interpol...",
      "confidence": 0.9
    },
    {
      "id": "e5",
      "type": "EMAIL",
      "value": "secure@banking-alerts.com",
      "description": "Phishing email address used in the scam.",
      "context": "The scam involved phishing emails sent from addresses like secure@banking-alerts.com...",
      "confidence": 0.95
    },
    {
      "id": "e6",
      "type": "EMAIL",
      "value": "cybercrime@justice.org",
      "description": "Fraud reporting email for victims to report scams.",
      "context": "Suspected fraud can be reported at cybercrime@justice.org...",
      "confidence": 0.9
    },
    {
      "id": "e7",
      "type": "PHONE",
      "value": "+1-800-123-4567",
      "description": "Fraudulent customer service number where victims were tricked into sharing sensitive information.",
      "context": "These emails tricked users into calling fraudulent customer service numbers like +1-800-123-4567...",
      "confidence": 0.95
    }
  ],
  "relationships": [
    {
      "source": "Brenda Wallace",
      "target": "FBI",
      "type": "INVESTIGATED_BY",
      "confidence": 0.9,
      "evidence": "A large-scale cyber fraud network was exposed in a joint operation by the FBI.",
      "strength": "STRONG"
    },
    {
      "source": "Brenda Wallace",
      "target": "+1-800-123-4567",
      "type": "CONTACTED",
      "confidence": 0.85,
      "evidence": "Victims were tricked into calling fraudulent customer service numbers like +1-800-123-4567.",
      "strength": "MEDIUM"
    }
  ],
  "anomalies": [
    {
      "description": "Use of burner phones by accomplices in the scam.",
      "severity": "HIGH",
      "related_entities": [
        "+1-555-987-6543",
        "+1-555-456-7890"
      ],
      "potential_impact": "These burner phones may point to further fraudulent activities and hidden criminal networks."
    }
  ],
  "graph_data": {
    "nodes": [
      { "id": "e1", "type": "PERSON", "value": "Brenda Wallace" },
      { "id": "e2", "type": "PERSON", "value": "Raj Patel" },
      { "id": "e3", "type": "ORGANIZATION", "value": "FBI" },
      { "id": "e4", "type": "ORGANIZATION", "value": "Interpol" },
      { "id": "e5", "type": "EMAIL", "value": "secure@banking-alerts.com" },
      { "id": "e6", "type": "EMAIL", "value": "cybercrime@justice.org" },
      { "id": "e7", "type": "PHONE", "value": "+1-800-123-4567" }
    ],
    "edges": [
      { "source": "e1", "target": "e3", "type": "INVESTIGATED_BY", "strength": "STRONG" },
      { "source": "e1", "target": "e7", "type": "CONTACTED", "strength": "MEDIUM" }
    ]
  }
}
🔍 Guidelines for OpenHermes
1. Extract & categorize entities:

Types: Persons, Organizations, Emails, Phone Numbers, Tools, Activities.
Context: Provide context from the text as evidence.
Confidence: Measure confidence level for each entity.
2. Relationships:

Form clear relationships (e.g., PERSON-to-ORGANIZATION, PERSON-to-PHONE, EMAIL-to-ORGANIZATION, etc.).
Use relationship types such as "INVESTIGATED_BY", "TARGETED_BY", "CONTACTED", "REPORTED_TO", "ASSOCIATED_WITH", etc.
Provide evidence (quotes from the text) for relationships.
3. Anomalies:

Highlight anomalies (like burner phones) and their potential impact.
Link anomalies to related entities and categorize severity (HIGH, MEDIUM, LOW).
4. Graph Data:

Nodes: Each entity is a node with a unique ID, type, and value. We need the nodes to be a array with the each node be a object with that specific entities information.
Edges: Each relationship is an edge, showing source, target, type, and strength. The edges is also a array with objects where it has the source and target. source is the person who is main and the target is who is related to by the relation.

5. Case Information:

Include case details (case number, title, date, etc.).


analyse this data and give responce as the same previous array json structure above containing the entities, relationships, anomalies, graph with nodes and edges, case info as per the structure not missing any most importantly the graph nodes and edges that are very important in the end result which is the inference from the entities,relations and anomalies: 

"""

    # Add documents with clear separation
    for i, doc in enumerate(documents, 1):
        print(doc)
        prompt += f"\n[Document {i}]\n{doc}\n"
    
    prompt += """\nCRITICAL REMINDERS:
1. NO isolated nodes allowed
2. EVERY entity must connect to at least 2 others
3. ALL relationships must have evidence
4. CREATE implicit relationships when logical
5. ENSURE complete network connectivity
6. USE only specified relationship types
7. INCLUDE full context in evidence
8. RETURN only valid JSON"""
    
    return prompt


def parse_response(response: Dict[str, Any]) -> DocumentAnalysisResponse:
    try:
        logger.info("Starting response parsing")
        
        content = response.get('response', '')
        if not content:
            raise ValueError("Empty response content")
            
        logger.info(f"Content length: {len(content)}")
        logger.debug(f"Raw content: {content[:500]}")

        json_start = content.find('{')
        json_end = content.rfind('}') + 1
        
        if json_start == -1 or json_end == 0:
            raise ValueError("No JSON object found in response")
            
        json_str = content[json_start:json_end]
        
        json_str = json_str.replace('```json', '').replace('```', '')
        json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
        
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            logger.debug(f"Attempted to parse: {json_str}")
            raise ValueError(f"Invalid JSON structure: {str(e)}")

        if "Document Summaries" in data and not any(k in data for k in ["entities", "relations", "anomalies"]):
  
            converted_data = {
                "entities": [],
                "relations": [],
                "anomalies": []
            }
            
            for summary in data["Document Summaries"]:
                if "Headline" in summary:
                    converted_data["entities"].append({
                        "value": summary["Headline"],
                        "type": "HEADLINE",
                        "context": summary.get("Summary", ""),
                        "confidence": 1.0
                    })
            
            data = converted_data

        data.setdefault("entities", [])
        data.setdefault("relations", [])
        data.setdefault("anomalies", [])

        entities = []
        for e in data.get("entities", []):
            try:
                entity = EntityModel(
                    value=str(e.get("value", "")).strip(),
                    type=str(e.get("type", "UNKNOWN")).strip(),
                    context=str(e.get("context", "")).strip(),
                    confidence=float(e.get("confidence", 0.5))
                )
                if entity.value:
                    entities.append(entity)
            except Exception as err:
                logger.warning(f"Error parsing entity: {e}. Error: {err}")

        relations = []
        for r in data.get("relations", []):
            try:
                relation = RelationModel(
                    source=str(r.get("source", "")).strip(),
                    target=str(r.get("target", "")).strip(),
                    type=str(r.get("type", "")).strip(),
                    confidence=float(r.get("confidence", 0.5))
                )
                if relation.source and relation.target:
                    relations.append(relation)
            except Exception as err:
                logger.warning(f"Error parsing relation: {r}. Error: {err}")

        anomalies = []
        for a in data.get("anomalies", []):
            try:
                anomaly = AnomalyModel(
                    description=str(a.get("description", "")).strip(),
                    severity=str(a.get("severity", "MEDIUM")).strip(),
                    related_entities=[str(e).strip() for e in a.get("related_entities", []) if str(e).strip()],
                    potential_impact=str(a.get("potential_impact", "")).strip() or None
                )
                if anomaly.description:
                    anomalies.append(anomaly)
            except Exception as err:
                logger.warning(f"Error parsing anomaly: {a}. Error: {err}")

        nodes = []
        edges = []
        entity_set = set()
        
        for entity in entities:
            if entity.value not in entity_set:
                nodes.append({
                    "id": entity.value,
                    "label": entity.value,
                    "type": entity.type,
                    "confidence": entity.confidence
                })
                entity_set.add(entity.value)

        for relation in relations:
            if relation.source in entity_set and relation.target in entity_set:
                edges.append({
                    "source": relation.source,
                    "target": relation.target,
                    "label": relation.type,
                    "confidence": relation.confidence
                })

        graph_data = GraphVizModel(nodes=nodes, edges=edges)
        
        logger.info(f"Successfully processed {len(entities)} entities, {len(relations)} relations, {len(anomalies)} anomalies")

        return DocumentAnalysisResponse(
            entities=entities,
            relations=relations,
            anomalies=anomalies,
            graph_data=graph_data
        )

    except Exception as e:
        logger.error(f"Error in parse_response: {str(e)}", exc_info=True)
        raise