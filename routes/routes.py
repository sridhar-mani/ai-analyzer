import ollama
from models.models import DocumentAnalysisRequest
from fastapi import File,UploadFile
from typing import List

@app.post("/analze")
async def analyze_doc(files: List[UploadFile] = File(...)):
    documents = []
    for f in files:
        content = await file.read()
        documents.append(content.decode('utf-8'))
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
    
    return parse_ollama_responce(responce)