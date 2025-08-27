from typing import Protocol

class IDocumentService(Protocol):
    def save(self, data: str, user_ids: list[int]) -> str: ...