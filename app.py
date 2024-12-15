from fastapi import FastAPI,UploadFile
from models.models import DocumentAnalysisRequest,DocumentAnalysisResponce
from fastapi.middleware.cors import CORSMiddleware
from routes.routes import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(router)