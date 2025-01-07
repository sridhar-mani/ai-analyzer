from langchain_community.embeddings import OllamaEmbeddings
from chromadb.utils.embedding_functions import EmbeddingFunction
from typing import List
import logging

logger = logging.getLogger(__name__)

class OllamaEmbeddingFunction(EmbeddingFunction):
    
    def __init__(self, model_name: str = "nomic-embed-text"):
        self.ollama_embeddings = OllamaEmbeddings(
            model=model_name,
            model_kwargs={"device": "cuda"}
        )
        
    def __call__(self, texts: List[str]) -> List[List[float]]:
        try:
            return self.ollama_embeddings.embed_documents(texts)
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise