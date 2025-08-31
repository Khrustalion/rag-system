from typing import Protocol

class IRAGService(Protocol):
    def generate_answer(self, query: str, user_id: int) -> str: ...