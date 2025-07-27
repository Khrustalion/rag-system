from rag.infrastructure.retriever import Retriever
from rag.domain import IGenerator
import os
import dotenv


class RAGService:
    def __init__(self, 
                 retriever: Retriever, 
                 generator: IGenerator) -> None:
        self.retriever = retriever
        self.generator = generator
        self.collection_name = str(os.getenv("COLLECTION_NAME"))


    def generate_answer(self, query: str, user_id: int) -> str:
        docs = "\n\n".join([f'{doc.date}\n{doc.text}' for doc in self.retriever.retrieve(query=query, user_id=user_id, collection_name=self.collection_name)])

        prompt = f"""Ответь на вопрос, используя только информацию из приведённого контекста.

                Делай выводы исключительно на основе текста. Отвечай максимально кратко и по делу.

                Если ответа нет в контексте или из него невозможно сделать никаких выводов, напиши: "Ответ не найден в контексте."

                Если ответ содержится в нескольких документах, используй версию из более свежего документа (с более поздней датой).

                Контекст:
                ===========
                {docs}
                ===========

                Вопрос:
                {query}"""
        
        answer = self.generator.generate(prompt, model="gpt-4.1-mini")

        return answer