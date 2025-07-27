from typing import Protocol


class IVectorizer(Protocol):
    def get_embedding(self, text: str) -> list[float]: ...