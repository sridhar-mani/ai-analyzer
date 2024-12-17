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
    prompt = """Extract and list the key entities (persons, organizations, phone numbers, emails) and their direct relationships (e.g., 'Carlos Ramirez' is 'CO-CONSPIRATOR' with 'Elena Torres') from the provided text. Present the data in a JSON format compatible with Cytoscape, including node identifiers, labels, and edge types.

Expected Output:

{
  "nodes": [
    {
      "data": {
        "id": "Carlos Ramirez",
        "label": "Carlos Ramirez",
        "type": "Person",
        "location": "New York",
        "contact": "+1-555-888-9999",
        "email": "carlos.ramirez@example.com",
        "affiliation": "XYZ Corp",
        "role": "Manager"
      }
    },
    {
      "data": {
        "id": "Elena Torres",
        "label": "Elena Torres",
        "type": "Person",
        "location": "Los Angeles",
        "contact": "+1-555-666-7777",
        "email": "elena.torres@example.com",
        "affiliation": "ABC Ltd",
        "role": "Analyst"
      }
    },
    {
      "data": {
        "id": "Kelly Johnson",
        "label": "Kelly Johnson",
        "type": "Person",
        "location": "Chicago",
        "contact": "+1-555-444-5555",
        "email": "kelly.johnson@example.com",
        "affiliation": "DEF Inc",
        "role": "Consultant"
      }
    },
    {
      "data": {
        "id": "Paul Simmons",
        "label": "Paul Simmons",
        "type": "Person",
        "location": "San Francisco",
        "contact": "+1-555-222-3333",
        "email": "paul.simmons@example.com",
        "affiliation": "GHI LLC",
        "role": "Director"
      }
    },
    {
      "data": {
        "id": "Agent Rebecca Cruz",
        "label": "Agent Rebecca Cruz",
        "type": "Person",
        "location": "Washington, D.C.",
        "contact": "+1-555-000-1111",
        "email": "rebecca.cruz@dea.gov",
        "affiliation": "DEA",
        "role": "Agent"
      }
    },
    {
      "data": {
        "id": "DEA",
        "label": "DEA",
        "type": "Organization",
        "location": "Washington, D.C.",
        "contact": "+1-800-DRUGSTOP",
        "email": "dea.tips@agency.gov",
        "affiliation": null,
        "role": null
      }
    }
  ],
  "edges": [
    {
      "data": {
        "source": "Carlos Ramirez",
        "target": "Elena Torres",
        "type": "CO-CONSPIRATOR",
        "relationship_strength": "High",
        "discovery_date": "2024-12-01"
      }
    },
    {
      "data": {
        "source": "DEA",
        "target": "Carlos Ramirez",
        "type": "ARRESTED",
        "relationship_strength": "N/A",
        "discovery_date": "2024-12-10"
      }
    },
    {
      "data": {
        "source": "DEA",
        "target": "Elena Torres",
        "type": "ARRESTED",
        "relationship_strength": "N/A",
        "discovery_date": "2024-12-10"
      }
    },
    {
      "data": {
        "source": "DEA",
        "target": "DEA",
        "type": "MONITORED_USING",
        "relationship_strength": "N/A",
        "discovery_date": "2024-12-05"
      }
    },
    {
      "data": {
        "source": "Carlos Ramirez",
        "target": "+1-555-888-9999",
        "type": "USED_FOR_COMMUNICATION",
        "relationship_strength": "High",
        "discovery_date": "2024-12-02"
      }
    },
    {
      "data": {
        "source": "Elena Torres",
        "target": "+1-555-666-7777",
        "type": "USED_FOR_COMMUNICATION",
        "relationship_strength": "Medium",
        "discovery_date": "2024-12-03"
      }
    },
    {
      "data": {
        "source": "DEA",
        "target": "dea.tips@agency.gov",
        "type": "CONTACT",
        "relationship_strength": "High",
        "discovery_date": "2024-12-01"
      }
    },
    {
      "data": {
        "source": "DEA",
        "target": "+1-800-DRUGSTOP",
        "type": "CONTACT",
        "relationship_strength": "High",
        "discovery_date": "2024-12-01"
      }
    }
  ]
}


Explanation:

Nodes: Each key entity is represented with a unique identifier (id) and a label (label).

Edges: Relationships between entities are defined with source and target nodes, along with a type indicating the nature of the relationship. 

I want you to analyse the below data and convert into the structure mentioned above:"""

    # Add documents with clear separation
    for i, doc in enumerate(documents, 1):
        print(doc)
        prompt += f"\n{doc}\n"
    
#     prompt += """\nCRITICAL REMINDERS:
# 1. NO isolated nodes allowed
# 2. EVERY entity must connect to at least 2 others
# 3. ALL relationships must have evidence
# 4. CREATE implicit relationships when logical
# 5. ENSURE complete network connectivity
# 6. USE only specified relationship types
# 7. INCLUDE full context in evidence
# 8. RETURN only valid JSON"""
    
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