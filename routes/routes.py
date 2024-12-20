
import ollama
import logging
import traceback
from typing import List
from fastapi import File, UploadFile, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from models.models import DocumentAnalysisRequest, DocumentAnalysisResponse, CaseInfo
from libs.prompt_and_parse import parse_response, create_extract_prompt
from libs.file_reader import UniversalDocumentReader
import hjson
from libs.prompt_and_parse import restructure_prompt


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()


MODELS = ["openhermes:latest", "mistral:instruct"]

@router.post("/analyze")
async def analyze_doc(files: List[UploadFile] = File(...)) -> dict:
    try:
        
        for f in files:
            try:
                logger.debug(f"Processing file: {f.filename}")
                content = await f.read()
                
                reader = UniversalDocumentReader(content, f.filename, f.file)
                document_data = reader.process_document()
                logger.debug(f"Document data: {document_data}")
                
                file_analysis = {
                    "filename": f.filename,
                    "cases": []
                }
                
                for case_id, case_data in document_data.get('cases', {}).items():
                    try:
                        logger.debug(f"Processing case: {case_id}")
                        case_content = case_data['content']
                        case_headline = case_data['headline']
                        case_data['page_number'] = case_id
                        
                        prompt = create_extract_prompt(case_headline, case_content)
                        
                        for model in MODELS:
                            try:
                                response = ollama.chat(
                                    model=model,
                                    messages=[{
                                        'role': 'system',
                                        'content': 'You are a skilled data analyst able to extract entity recognition, relationship extraction and anomaly detection'
                                    }, {
                                        'role': 'user',
                                        'content': prompt
                                    }],
                                    options={
                                        "num_predict": 4096,
                                        "stop": ["\n\n\n"],
                                        "temperature": 0.7
                                    }
                                )
                                
                                if hasattr(response, 'message'):
                                    content = response.message.content
                                    if content:
                                        parsed_response = parse_response({'response': content})
                                        if parsed_response:
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
        print('--------------------------------------------file analyssis final output ------------------------------------------------')
        
        print(file_analysis)

        print('--------------------------------------------file analyssis final output ------------------------------------------------')
        
        return JSONResponse({"status":"success","data":file_analysis})
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Error processing request: {str(e)}"}
        )