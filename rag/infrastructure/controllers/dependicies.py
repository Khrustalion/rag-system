from openai import OpenAI

from qdrant_client import QdrantClient

from dotenv import load_dotenv
import os

from rag.infrastructure.retriever import Retriever, VectorizerOpenAI, GeneratorOpenAI
from rag.infrastructure.repositories import QdrantRepository, RepositoryAA
from rag.infrastructure.services import RAGService, RAGServiceAA, DocumentService

from typing import Annotated

def get_rag_service(openai_client: OpenAI):
    load_dotenv()

    qdrant_client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API"))
    qdrant_repository = QdrantRepository(qdrant_client)

    vectorizer = VectorizerOpenAI(openai_client)
    llm = GeneratorOpenAI(openai_client)

    retriever = Retriever(qdrant_repository, vectorizer, llm, doc_limit=5)

    return RAGService(retriever, llm)

def get_openai_client():
    load_dotenv()

    return OpenAI(api_key=os.getenv("PROXYAPI_KEY"), base_url="https://api.proxyapi.ru/openai/v1")


def get_document_service(openai_client: OpenAI):
    repository = RepositoryAA(openai_client)

    return DocumentService(repository)
    
    

def get_rag_service_aa(openai_client: OpenAI):
    load_dotenv()
    instructions = """"Вы — Ассистент по внутренним документам компании. Ваша единственная задача — отвечать на вопросы пользователя, извлекая информацию из внутренних документов с помощью встроенного vector_store.

                Правила работы:

                1. При каждом запросе формируйте и выполняйте поиск по vector_store, включающий полную формулировку вопроса пользователя и ключевые термины из диалога.  
                2. Если по запросу нет релевантных результатов, ответьте: «Извините, я не нашёл информацию по этому запросу в доступных документах.»  
                3. Не добавляйте сведений извне, не придумывайте ответы и не раскрывайте посторонние данные — работайте только с загруженными документами.  
                4. Отвечайте чётко, кратко и по существу заданного вопроса.  
                """

    assistant = openai_client.beta.assistants.create(
        name="Smart Assistant",
        model="gpt-4.1-mini",
        instructions=instructions,
        tools=[{
            "type": "file_search"
    }])

    os.makedirs("/data", exist_ok=True)

    if not os.path.exists("/data/assistants"):
        open("/data/assistants", "w+").close()

    with open("/data/assistants", "a") as f:
        f.write(f"assistant: {assistant.id}\n")


    return RAGServiceAA(openai_client, assistant)

