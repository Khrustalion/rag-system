from typing import Protocol
from typing import Sequence
from typing import Optional

from rag.domain.models import Document


class IDocumentRepository(Protocol):
    def save(self, vector: list[float], document: Document, collection_name: str) -> None: ...
    def get_by_id(self, doc_id: str, collection_name: str) -> Optional[Document]: ...
    def search(self, vector: Sequence[float], user_id: int,  limit: int, collection_name: str) -> list[Document]: ...