from dataclasses import dataclass
from datetime import datetime

@dataclass
class Document:
    id: str
    text: str
    req_id: str
    users_id: list[int]
    date: datetime