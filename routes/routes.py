import json
import ollama
import logging
import traceback
from typing import List,Dict,Union, Optional
from fastapi import File, HTTPException, APIRouter, Form, Request
from fastapi.responses import JSONResponse
from models.models import CaseInfo
from libs.prompt_and_parse import parse_response, create_extract_prompt
from libs.file_reader import UniversalDocumentReader
from libs.case_processor import CaseProcessor
import hjson
from starlette.datastructures import UploadFile
import re


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()



case_processor = CaseProcessor()

MODELS = ["deepseek-r1:8b","openhermes:latest", "mistral:instruct"]

@router.post("/analyze")
async def analyze_doc(request:Request) -> dict:
    case_id=0
    form_data = await request.form()
    form_data = form_data.items()
    files =[]
    data={}
    for key,value in dict(form_data).items():
        if isinstance(value,UploadFile):
            files.append(value)
        if isinstance(value,str):
            data[key] = value

    try:
        all_analysis = []

        print(data)
        if files:
            for f in files:

                try:

                    content = f.file.read()
                    
                    reader = UniversalDocumentReader(content, f.filename, f.file)
                    document_data = reader.process_document()
                    logger.debug(f"Document data: {document_data}")
                    
                    file_analysis = {
                        "filename": f.filename,
                        "cases": []
                    }
                    
                    for c_id, case_data in document_data.get('cases', {}).items():
                        try:
                            
                            logger.debug(f"Processing case: {c_id}")
                            case_content = case_data['content']
                            case_headline = case_data['headline']
                            case_data['page_number'] = c_id

                            initial_analysis = case_processor.analyze_case({
                                'headline':case_headline,
                                'content':case_content
                            })

                            similar_cases = initial_analysis.get('similar_cases',[])
                            
                            enchanced_prompt = f"""
                            Similar case for reference:
                            {json.dumps(similar_cases,indent=2)}

                            Based on these similar cases, analyze the following case:
                            """
                            

                            prompt = create_extract_prompt(case_headline, case_content)
                            full_prompt = enchanced_prompt+prompt
                            
                            for model in MODELS:
                                try:
                                    response = ollama.chat(
                                        model=model,
                                        messages=[{
                                            'role': 'system',
                                            'content': 'You are a skilled data analyst able to extract entity recognition, relationship extraction and anomaly detection'
                                        }, {
                                            'role': 'user',
                                            'content': full_prompt
                                        }],
                                        options={
                                            "num_predict": 4096,
                                            "stop": ["\n\n\n"],
                                            "temperature": 0
                                        },
                                     format={
        "type": "object",
        "properties": {
            "nodes": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "string",
                            "description": "Unique identifier for the node"
                        },
                        "label": {
                            "type": "string",
                            "description": "Display name or label for the node"
                        },
                        "type": {
                            "type": "string",
                            "description": "Type of entity (Person, Organization, Object, etc.)"
                        },
                        "location": {
                            "type": "string",
                            "description": "Location associated with the entity"
                        },
                        "contact": {
                            "type": "string",
                            "description": "Contact information if available"
                        },
                        "affiliation": {
                            "type": "string",
                            "description": "Any organizational affiliations"
                        },
                        "value": {
                            "type": "string",
                            "description": "Value or amount if applicable"
                        }
                    },
                    "required": ["id", "label", "type", "location"]
                }
            },
            "edges": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "source": {
                            "type": "string",
                            "description": "ID of the source node"
                        },
                        "target": {
                            "type": "string",
                            "description": "ID of the target node"
                        },
                        "type": {
                            "type": "string",
                            "description": "Type of relationship"
                        },
                        "relationship_strength": {
                            "type": "string",
                            "description": "Strength of the relationship (High, Medium, Low)"
                        }
                    },
                    "required": ["source", "target", "type", "relationship_strength"]
                }
            }
        },
        "required": ["nodes", "edges"]
    }
                                    )
                                    
                                    if hasattr(response, 'message'):
                                        content = response.message.content
                                        if content:
                                            parsed_response = parse_response({'response': content})
                                            if parsed_response:
                                                case_processor.store_successful_case(
                                                    case_content,
                                                    initial_analysis['type'],
                                                    parsed_response
                                                )
                                                break
                                        else:
                                            logger.warning(f"Empty content for case {c_id} using model {model}")
                                    else:
                                        logger.warning(f"No message attribute in response for case {c_id} using model {model}")
                                except Exception as e:
                                    logger.warning(f"Error using model {model} for case {c_id}: {str(e)}")
                            
                            case_info = CaseInfo(
                                case_id=c_id,
                                headline=case_headline,
                                page_number=case_data['page_number'],
                                content=case_content,
                                ai_analysis=parsed_response
                            )
                            
                            file_analysis["cases"].append(case_info)
                            
                        except Exception as e:
                            logger.error(f"Error processing case {case_id}: {str(e)}")
                            logger.error(traceback.format_exc())
                            continue
                except Exception as e:
                    logger.error(f"Error processing file {f.filename}: {str(e)}")
                    logger.error(traceback.format_exc())
                    continue
                all_analysis.append(file_analysis)
            print('--------------------------------------------file analyssis final output ------------------------------------------------')
            
            print(file_analysis)

            print('--------------------------------------------file analyssis final output ------------------------------------------------')
        
        if data:
            try:

                            case_content = data['content']
                            case_headline = data['headline']

                            file_analysis = {
                        "filename": "Prompted",
                        "cases": []
                    }

                            case_content = re.split(r'(?<=[.!?])\s+',case_content)


                            initial_analysis = case_processor.analyze_case({
                                'headline':case_headline,
                                'content':case_content
                            })

                            similar_cases = initial_analysis.get('similar_cases',[])
                            
                            enchanced_prompt = f"""
                            Similar case for reference:
                            {json.dumps(similar_cases,indent=2)}

                            Based on these similar cases, analyze the following case:
                            """
                            

                            prompt = create_extract_prompt(case_headline, case_content)
                            full_prompt = enchanced_prompt+prompt
                            
                            for model in MODELS:
                                try:
                                    response = ollama.chat(
                                        model=model,
                                        messages=[{
                                            'role': 'system',
                                            'content': 'You are a skilled data analyst able to extract entity recognition, relationship extraction and anomaly detection'
                                        }, {
                                            'role': 'user',
                                            'content': full_prompt
                                        }],
                                        options={
                                            "num_predict": 4096,
                                            "stop": ["\n\n\n"],
                                            "temperature": 0.3
                                        }
                                    )
                                    
                                    if hasattr(response, 'message'):
                                        content = response.message.content
                                        if content:
                                            parsed_response = parse_response({'response': content})
                                            if parsed_response:
                                                case_processor.store_successful_case(
                                                    case_content,
                                                    initial_analysis['type'],
                                                    parsed_response
                                                )
                                                break
                                        else:
                                            logger.warning(f"Empty content for case {case_id} using model {model}")
                                    else:
                                        logger.warning(f"No message attribute in response for case {case_id} using model {model}")
                                except Exception as e:
                                    logger.warning(f"Error using model {model} for case {case_id}: {str(e)}")
                            
                            case_info = CaseInfo(
                                case_id=case_id,
                                headline=case_headline,
                                page_number=1,
                                content=case_content,
                                ai_analysis=parsed_response
                            )
                            
                            file_analysis["cases"].append(case_info)
                            
                        
            except Exception as e:
                            logger.error(f"Error processing case {case_id}: {str(e)}")
                            logger.error(traceback.format_exc())
        return ({
            "status":"success",
            "data":[file_analysis]
        })
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Error processing request: {str(e)}"}
        )