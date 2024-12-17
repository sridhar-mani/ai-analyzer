# routes.py
import ollama
import logging
import traceback
from typing import List
from fastapi import File, UploadFile, HTTPException, APIRouter
from models.models import DocumentAnalysisRequest, DocumentAnalysisResponse, CaseInfo
from libs.prompt_and_parse import parse_response, create_extract_prompt
from libs.file_reader import UniversalDocumentReader

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/analyze")
async def analyze_doc(files: List[UploadFile] = File(...)) -> List[DocumentAnalysisResponse]:
    try:
        all_analyses = []
        
        for f in files:
            try:
                logger.debug(f"Processing file: {f.filename}")
                content = await f.read()
                
                reader = UniversalDocumentReader(content, f.filename,f.file)
                document_data = reader.process_document()
                logger.debug(f"Document data: {document_data}")
                
                for case in document_data.get('cases', []):
                    try:
                        logger.debug(f"Processing case: {case}")
                        case_content = document_data['cases'][case]['content']
                        case_headline = document_data['cases'][case]['headline']
                        
                        prompt = create_extract_prompt(case_headline,case_content)
                        logger.debug(f"Created prompt for case: {case_headline}")
                        
                        response = ollama.chat(
                            model="openhermes:latest",
                            messages=[{
                                'role': 'user',
                                'content': prompt
                            }]
                        )
                        
                        if hasattr(response, 'message'):
                            content = response.message.content
                            
                            if not content:
                                logger.warning(f"Empty response for case: {case_headline}")
                                continue
                            
                            logger.debug(f"Got response for case: {case_headline}")
                            
                            result = parse_response({'response': content})
                            
                            case_info = CaseInfo(
                                headline=case_headline,
                                type=case['analysis']['type'],
                                page_number=case['page_number']
                            )
                            
                            result.case_info = case_info
                            
                            all_analyses.append(result)
                            
                    except Exception as e:
                        logger.error(f"Error processing case {case_headline}: {str(e)}")
                        logger.error(traceback.format_exc())
                        continue
                    
            except Exception as e:
                logger.error(f"Error processing file {f.filename}: {str(e)}")
                logger.error(traceback.format_exc())
                continue
        
        if not all_analyses:
            raise ValueError("No valid analyses produced")
            
        return all_analyses
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )