from openai import OpenAI

from qdrant_client import QdrantClient

from dotenv import load_dotenv
import os

from rag.infrastructure.retriever import Retriever, VectorizerOpenAI, GeneratorOpenAI
from rag.infrastructure.repositories import QdrantRepository
from rag.infrastructure.services import RAGService

def get_rag_service():
    load_dotenv()

    qdrant_client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API"))
    qdrant_repository = QdrantRepository(qdrant_client)

    openai_client = OpenAI(api_key=os.getenv("PROXYAPI_KEY"), base_url="https://api.proxyapi.ru/openai/v1")
    vectorizer = VectorizerOpenAI(openai_client)
    llm = GeneratorOpenAI(openai_client)

    retriever = Retriever(qdrant_repository, vectorizer, llm, doc_limit=5)

    return RAGService(retriever, llm)
