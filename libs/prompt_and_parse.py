from typing import List, Dict, Any
import json
import re
import logging
import hjson
import ollama
from ast import literal_eval
import jsonfinder
import demjson3

logger = logging.getLogger(__name__)

def create_extract_prompt(headline: List[str],content: str) -> str:
    prompt = """For this task, process a given paragraph or case scenario and generate a structured output that highlights the key entities, their relationships, and the phases of the event. The input text can describe various types of events such as criminal investigations, business operations, or general cases involving people, organizations, and actions. Your goal is to identify entities like people, locations, organizations, and objects, and map out the relationships between them. Additionally, break down the event into phases like discovery, investigation, intervention, and resolution.

Steps for Processing the Input:
Entity Extraction:

People (Actors):
Witnesses: Individuals who observe or are aware of the events or incidents.
Suspects/Targets: Individuals or entities under suspicion or investigation.
Investigators/Agents: Entities actively investigating or tracking the case.
External Agents/Agencies: External organizations or public entities involved in the situation (e.g., NGOs, public organizations, or online platforms).
Organizations:
Involved Entities: Any organization linked to the event (e.g., criminal organizations, companies, law enforcement agencies, etc.).
Collaborating Entities: Organizations or groups that assist in the investigation or resolution of the case (e.g., another law enforcement body, tech companies, public agencies).
Locations:
Primary Locations: Locations where the event takes place or where significant actions occur (e.g., crime scene, meeting point, warehouse).
Secondary Locations: Locations that are indirectly connected to the case (e.g., storage locations, affiliated sites, or homes of suspects).
Objects/Tools:
Physical Evidence: Items linked directly to the event (e.g., stolen goods, weapons, tools).
Technology: Devices or systems involved in the event, such as phones, apps, or digital platforms used for coordination.
Communication Devices: Technologies such as burner phones, email addresses, or encrypted messaging services used to facilitate the event.
Relationship Extraction: Identify and categorize the relationships between the extracted entities to map how they are connected in the context of the situation. These include:

Communication: Instances where entities communicate or exchange information.
Coordination: Collaboration or work between entities for a shared goal.
Affiliation: Connections between individuals and organizations or among different organizations.
Surveillance/Investigation: Tracking or monitoring by law enforcement or other authorities.
Conflict/Disagreement: Tension or opposition between entities (e.g., rival gangs, competing interests).
Impact/Outcome:

Execution/Action: Physical actions such as arrests, raids, or discoveries.
Reporting/Announcement: Communication of findings, either by investigators or public entities.
Resolution: The conclusion of the case or event, including arrests, dismantling of organizations, or public statements.
Action/Event Phases:

Discovery: The initial moment when the event is first noticed or detected (e.g., observation of suspicious activity, discovery of evidence, or identification of a suspect).
Investigation: The phase where authorities or investigators begin their work, such as gathering evidence, conducting interviews, or monitoring suspects.
Intervention/Execution: Significant actions happen, such as arrests, raids, or the interception of a communication.
Reporting/Resolution: The final phase where results are made public, the event concludes, and outcomes like arrests or dismantling of criminal activity are announced.
Example Input:
"A multi-state drug trafficking operation was uncovered during an extensive investigation by federal authorities. The investigation started when a suspicious van was seen in a remote warehouse area, and further surveillance led to the discovery of drugs worth millions of dollars. Authorities traced the drugs back to a major distributor operating across state lines. Several arrests were made, and more suspects are under investigation. The authorities have urged the public to stay vigilant and report any suspicious activities."

Make sure the source are target of each edge is present as a node in the node array without any repitition. Make sure to keep the processing of one data from another so that you don't repeat any responce for each case.

Expected Output Format:
json
Copy code
{
  "nodes": [
    {
      "id": "Witness",
      "label": "Witness",
      "type": "Person",
      "location": "Warehouse Area",
      "contact": "Phone Number or Anonymous"
    },
    {
      "id": "Suspect",
      "label": "Suspect",
      "type": "Person",
      "location": "State X",
      "affiliation": "Criminal Organization"
    },
    {
      "id": "Investigator",
      "label": "Federal Authorities",
      "type": "Organization",
      "location": "Headquarters"
    },
    {
      "id": "Drug",
      "label": "Illegal Narcotics",
      "type": "Object",
      "value": "Millions of dollars"
    }
  ],
  "edges": [
    {
      "source": "Witness",
      "target": "Investigator",
      "type": "Reports Suspicious Activity",
      "relationship_strength": "High"
    },
    {
      "source": "Suspect",
      "target": "Criminal Organization",
      "type": "Affiliated With",
      "relationship_strength": "High"
    },
    {
      "source": "Investigator",
      "target": "Criminal Organization",
      "type": "Investigates",
      "relationship_strength": "High"
    },
    {
      "source": "Public",
      "target": "Authorities",
      "type": "Reports Suspicious Activity",
      "relationship_strength": "Medium"
    }
  ],
  "event_phases": [
    {
      "phase": "Discovery",
      "description": "Suspicious van and remote warehouse area."
    },
    {
      "phase": "Investigation",
      "description": "Surveillance leading to the discovery of drugs and the identification of the distributor."
    },
    {
      "phase": "Intervention",
      "description": "Arrests and ongoing investigations."
    },
    {
      "phase": "Resolution",
      "description": "Public urged for vigilance and announcement of arrests."
    }
  ]
}
  "end": []
}"""

    prompt+=f"\n Headline of the data: {headline}\n"
    content = "".join(content)
    prompt+=f'Content of the data: {content}'
    
    
    return prompt


def parse_response(response: Dict[str, Any]) -> dict:
    try:
        logger.info("Starting response parsing")
        
        content = response.get('response', '')
        if not content:
            raise ValueError("Empty response content")
            
        logger.info(f"Content length: {len(content)}")
        logger.debug(f"Raw content: {content[:500]}")

        json_cleaned = content.replace('\n', '').replace('\r', '')
        
        json_cleaned=json_cleaned.replace('```','')
        if 'Nodes:' in json_cleaned:
          json_cleaned = '{"nodes"'+json_cleaned.split('nodes')[1]
        else:
          json_cleaned = '{"nodes"'+json_cleaned.split('"nodes"')[1]
            

        # Try loading the cleaned JSON with hjson, falling back to json
        try:
            data = demjson3.decode(json_cleaned, strict=False)
        except hjson.HjsonDecodeError:
            try:
                data = jsonfinder.JSONFinder(json_cleaned)
            except json.JSONDecodeError:
                logger.error("Failed to parse JSON or HJSON")
                raise ValueError("Failed to parse JSON or HJSON")

        # Extract nodes and edges, ensure correct structure
        nodes = data.get('nodes', [])
        edges = data.get('edges', [])

        # Assuming GraphVizModel can be created with nodes and edges (you can adjust this as needed)
        graph_data = {
            'nodes': nodes,
            'edges': edges
        }

        return  graph_data

    except Exception as e:
        logger.error(f"Error in parse_response: {str(e)}", exc_info=True)
        raise