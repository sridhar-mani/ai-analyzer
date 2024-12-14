from fastapi import FastAPI,UploadFile
from models.models import DocumentAnalysisRequest,DocumentAnalysisResponce
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)