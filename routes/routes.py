import ollama
from models.models import DocumentAnalysisRequest
from fastapi import File,UploadFile,HTTPException, APIRouter
from typing import List
from libs.prompt_and_parse import parse_responce,create_extract_prompt,preprocess_document
from libs.file_reader import UniversalDocumentReader


router = APIRouter()

@router.post("/analyze")
async def analyze_doc(files: List[UploadFile] = File(...)):
    try:
        documents = []
        for f in files:
            content = await f.read()
            reader = UniversalDocumentReader(content, f.filename)
            file_lines=list(reader.read_lines())
            documents.append("\n".join(file_lines))
        request = DocumentAnalysisRequest(documents=documents)
        
        responce = ollama.chat(
            model="mistral:instruct",
            messages=[
                {
                    'role':'user',
                    'content':create_extract_prompt(request.documents)
                }
            ]
        )
        
        return parse_responce(responce)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))