from langchain_community.embeddings import OllamaEmbeddings
from chromadb.utils.embedding_functions import EmbeddingFunction
from typing import List
import logging

logger = logging.getLogger(__name__)

class OllamaEmbeddingFunction(EmbeddingFunction):
    
    def __init__(self, model_name: str = "nomic-embed-text"):
        self.ollama_embeddings = OllamaEmbeddings(
            model=model_name,
            model_kwargs={"device": "cuda","output_dim": 768}
        )
        
    def __call__(self, texts: List[str]) -> List[List[float]]:
        try:
            embeding = self.ollama_embeddings.embed_documents(texts)
            return embeding
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise