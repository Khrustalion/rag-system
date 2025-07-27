from rag.domain.i_document_repository import IDocumentRepository ,Document
from rag.domain.i_vectorizer import IVectorizer
from rag.domain.i_generator  import IGenerator

import os

class Retriever:
    def __init__(self, docRepository: IDocumentRepository, vectorizer: IVectorizer, generator: IGenerator, doc_limit: int = 5) -> None:
        self.docRepository = docRepository
        self.vectorizer = vectorizer
        self.generator = generator
        self.doc_limit = doc_limit

    
    def retrieve(self, query: str, user_id: int, collection_name: str) -> list[Document]:
        hypotetical_doc = self.generator.generate(self._build_hypothetical_doc(query), model="gpt-4.1-mini", temperature=0)

        query_vector = self.vectorizer.get_embedding(hypotetical_doc)

        return self.docRepository.search(query_vector, user_id=user_id, limit=self.doc_limit, collection_name=collection_name)
    

    def _build_hypothetical_doc(self, query: str) -> str:
        prompt = f"""Ты — помощник, который должен написать гипотетический фрагмент документа, в котором содержится информация, отвечающая на вопрос ниже.

        Вопрос: {query}

        Сгенерируй реалистичный, информативный текст, в котором упоминаются ключевые элементы вопроса — включая имена, даты и действия. Пиши так, как если бы этот текст был частью отчёта, биографии, статьи или другого документа, который потенциально может содержаться в базе знаний.

        Не объясняй, что ты отвечаешь на вопрос — просто напиши содержательное повествование.

        Тон: нейтральный, деловой.
        """
        
        return prompt

        
