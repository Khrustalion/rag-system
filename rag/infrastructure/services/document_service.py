from rag.infrastructure.repositories import RepositoryAA

class DocumentService:
    def __init__(self, repository: RepositoryAA):
        self.repository = repository


    def save(self, data: str, filename: str, user_ids: list[int]) -> str:
        return self.repository.save(data, filename, user_ids)