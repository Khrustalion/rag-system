from pydantic import BaseModel
from typing import Optional


class PostRequest(BaseModel):
    query: str
    user_id: int


class PostResponse(BaseModel):
    text: str
    user_id: int