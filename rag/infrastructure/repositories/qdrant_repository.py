from typing import Protocol
from typing import Sequence
from typing import Optional

from rag.domain.models import Document
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, MatchValue, FieldCondition
import uuid

from datetime import datetime


class QdrantRepository:
    def __init__(self, client: QdrantClient) -> None:
        self.client = client

    
    def save(self, vector: list[float], document: Document, collection_name: str) -> None:
        payload = {
            "text" : document.text,
            "req_id" : document.req_id,
            "users_id" : document.users_id,
            "date": document.date.strftime("%Y:%m:%d %H:%M:%S")
        }

        self.client.upsert(
            collection_name=collection_name,
            points=[
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload=payload
                )
            ]
        )

    def get_by_id(self, doc_id: str, collection_name: str) -> Optional[Document]:
        result = self.client.retrieve(collection_name=collection_name, ids=[doc_id])

        if not result or not result[0] or not result[0].payload:
            return None

        return Document(str(result[0].id), result[0].payload['text'], result[0].payload['req_id'], result[0].payload['users_id'], result[0].payload['date'])


    def search(self, vector: Sequence[float], user_id: int,  limit: int, collection_name: str) -> list[Document]:
        filter = Filter(
            must=[
                FieldCondition(
                    key="users_id",
                    match=MatchValue(value=user_id)
                )
                ]
        )

        result = self.client.search(collection_name=collection_name, query_vector=vector, limit=limit, query_filter=filter)

        return [
            Document(
                str(doc.id),
                doc.payload['text'],
                doc.payload['req_id'],
                doc.payload['users_id'],
                datetime.strptime(doc.payload['date'], "%Y:%m:%d %H:%M:%S")
            )
            for doc in result
        ]

