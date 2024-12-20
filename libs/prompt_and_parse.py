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
    prompt = """Extract and list the key entities (persons, organizations, phone numbers, emails) and their direct relationships (e.g., 'Carlos Ramirez' is 'CO-CONSPIRATOR' with 'Elena Torres') from the provided text. Present the data in a JSON format compatible with Cytoscape, including node identifiers, labels, and edge types.

Expected Output:

{
  "nodes": [
    {

        "id": "Carlos Ramirez",
        "label": "Carlos Ramirez",
        "type": "Person",
        "location": "New York",
        "contact": "+1-555-888-9999",
        "email": "carlos.ramirez@example.com",
        "affiliation": "XYZ Corp",
        "role": "Manager"

    },
    {
 
        "id": "Elena Torres",
        "label": "Elena Torres",
        "type": "Person",
        "location": "Los Angeles",
        "contact": "+1-555-666-7777",
        "email": "elena.torres@example.com",
        "affiliation": "ABC Ltd",
        "role": "Analyst"

    },
    {

        "id": "Kelly Johnson",
        "label": "Kelly Johnson",
        "type": "Person",
        "location": "Chicago",
        "contact": "+1-555-444-5555",
        "email": "kelly.johnson@example.com",
        "affiliation": "DEF Inc",
        "role": "Consultant"
  
    },
    {
     
        "id": "Paul Simmons",
        "label": "Paul Simmons",
        "type": "Person",
        "location": "San Francisco",
        "contact": "+1-555-222-3333",
        "email": "paul.simmons@example.com",
        "affiliation": "GHI LLC",
        "role": "Director"
   
    },
    {
  
        "id": "Agent Rebecca Cruz",
        "label": "Agent Rebecca Cruz",
        "type": "Person",
        "location": "Washington, D.C.",
        "contact": "+1-555-000-1111",
        "email": "rebecca.cruz@dea.gov",
        "affiliation": "DEA",
        "role": "Agent"
  
    },
    {
    
        "id": "DEA",
        "label": "DEA",
        "type": "Organization",
        "location": "Washington, D.C.",
        "contact": "+1-800-DRUGSTOP",
        "email": "dea.tips@agency.gov",
        "affiliation": null,
        "role": null

    }
  ],
  "edges": [
    {
 
        "source": "Carlos Ramirez",
        "target": "Elena Torres",
        "type": "CO-CONSPIRATOR",
        "relationship_strength": "High",
        "discovery_date": "2024-12-01"
  
    },
    {
     
        "source": "DEA",
        "target": "Carlos Ramirez",
        "type": "ARRESTED",
        "relationship_strength": "N/A",
        "discovery_date": "2024-12-10"
  
    },
    {
     
        "source": "DEA",
        "target": "Elena Torres",
        "type": "ARRESTED",
        "relationship_strength": "N/A",
        "discovery_date": "2024-12-10"

    },
    {

        "source": "DEA",
        "target": "DEA",
        "type": "MONITORED_USING",
        "relationship_strength": "N/A",
        "discovery_date": "2024-12-05"

    },
    {

        "source": "Carlos Ramirez",
        "target": "+1-555-888-9999",
        "type": "USED_FOR_COMMUNICATION",
        "relationship_strength": "High",
        "discovery_date": "2024-12-02"

    },
    {
        "source": "Elena Torres",
        "target": "+1-555-666-7777",
        "type": "USED_FOR_COMMUNICATION",
        "relationship_strength": "Medium",
        "discovery_date": "2024-12-03"

    },
    {
        "source": "DEA",
        "target": "dea.tips@agency.gov",
        "type": "CONTACT",
        "relationship_strength": "High",
        "discovery_date": "2024-12-01"
    },
    {
        "source": "DEA",
        "target": "+1-800-DRUGSTOP",
        "type": "CONTACT",
        "relationship_strength": "High",
        "discovery_date": "2024-12-01"
    }
  ]
}


Explanation:

Nodes: Each key entity is represented with a unique identifier (id) and a label (label).

Edges: Relationships between entities are defined with source and target nodes, along with a type indicating the nature of the relationship.

Make sure to give only the json string output no text other than that and the main json should have 2 properties the nodes and edges. Nodes should have a array that has objects each a node. Edges should have a array that has objects each a edge.

I want you to analyse the below data and convert into the structure mentioned above:"""

    # Add documents with clear separation
    prompt+=f"\n Headline of the data: {headline}\n"
    content = "".join(content)
    prompt+=f'Content of the data: {content}'
    
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


def restructure_prompt(original_prompt):
    improvement_prompt = f"""
    As an AI language model expert, your task is to analyze and improve the following prompt. 
    The prompt is designed to extract entity recognition, relationship extraction, and anomaly detection from legal case content.
    Please suggest improvements to make the prompt more effective, clear, and likely to yield accurate results.

    Original Prompt:
    {original_prompt}

    Please provide an improved version of this prompt, addressing the following aspects:
    1. Clarity: Ensure the instructions are clear and unambiguous.
    2. Specificity: Add more specific guidelines for entity recognition, relationship extraction, and anomaly detection.
    3. Structure: Improve the structure to make it easier for the model to follow and respond accurately.
    4. Completeness: Add any missing elements that could help in getting a more comprehensive analysis.

    Provide only the improved prompt without any additional explanations.
    """

    try:
        response = ollama.chat(
            model="mistral:instruct",
            messages=[
                {
                    'role': 'system',
                    'content': 'You are an expert AI prompt engineer, skilled at improving prompts for optimal results.'
                },
                {
                    'role': 'user',
                    'content': improvement_prompt
                }
            ],
            options={
                "num_predict": 4096,
                "stop": ["\n\n\n"],
                "temperature": 0.7
            }
        )

        if hasattr(response, 'message'):
            improved_prompt = response.message.content.strip()
            logger.info("Successfully restructured the prompt")
            return improved_prompt
        else:
            logger.warning("Failed to get a response for prompt restructuring")
            return original_prompt

    except Exception as e:
        logger.error(f"Error in restructuring prompt: {str(e)}")
        return original_prompt


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