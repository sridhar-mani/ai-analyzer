import ollama
from models.models import DocumentAnalysisRequest
from fastapi import File,UploadFile,HTTPException
from typing import List
from libs.prompt_and_parse import parse_responce,create_extract_prompt,preprocess_document
from app import app

@app.post("/analyze")
async def analyze_doc(files: List[UploadFile] = File(...)):
    try:
        documents = []
        for f in files:
            content = await f.read()
            preprocessed_content= preprocess_document(content.decode('utf-8'))
            documents.append(preprocessed_content)
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