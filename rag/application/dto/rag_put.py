from pydantic import BaseModel, Field
from typing import Optional


class PutRequest(BaseModel):
    data: str = Field(..., min_length=1)
    filename: str = Field(..., pattern=r".+\..+")
    user_ids: list[int] = Field(..., min_length=1)


class PutResponse(BaseModel):
    file_id: str
    user_ids: list[int]