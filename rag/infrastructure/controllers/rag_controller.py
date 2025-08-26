from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse

from rag.infrastructure.services import RAGService
from rag.infrastructure.controllers import get_rag_service_aa
from rag.application.dto import PostRequest, PostResponse

router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


@router.post("/generate_answer")
def generate_answer(
    dto_request: PostRequest,
    rag_service: Annotated[RAGService, Depends(get_rag_service_aa)],
):
    try:
        query: str = dto_request.query
        answer = rag_service.generate_answer(query, dto_request.user_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while generation: {e}.")

    return PostResponse(text=answer, user_id=dto_request.user_id)