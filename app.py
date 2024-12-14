from fastapi import FastAPI,UploadFile
from models.models import DocumentAnalysisRequest,DocumentAnalysisResponce
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.app_middleware(
    CORSMiddleware,
    allowed_origins=['*'],
    allowed_credentials=True,
    allowed_methods=['*'],
    allowed_headers=['*']
)