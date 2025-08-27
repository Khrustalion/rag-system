from fastapi import APIRouter, HTTPException, Request

from rag.application.dto import PostRequest, PostResponse, PutResponse, PutRequest

router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)

SUPPORTED_EXT = {"txt","md","pdf","csv","json","docx","pptx","xlsx","html"}

def _validate_filename(name: str) -> None:
    if not name or "." not in name:
        raise HTTPException(400, "Filename must include an extension (e.g., document.txt).")
    ext = name.rsplit(".", 1)[-1].lower()
    if ext not in SUPPORTED_EXT:
        raise HTTPException(415, f"Extension .{ext} is not supported for retrieval.")


@router.post("/generate_answer")
def generate_answer(
    dto_request: PostRequest,
    request: Request,
):
    try:
        query: str = dto_request.query
        answer = request.app.state.rag_service.generate_answer(query, dto_request.user_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while generation: {e}.")

    return PostResponse(text=answer, user_id=dto_request.user_id)


@router.put("/text/upload")
def add_text(
    dto_request: PutRequest,
    request: Request
):
    try:
        file_id = request.app.state.doc_service.save(dto_request.data, dto_request.filename, dto_request.user_ids)
        return PutResponse(file_id=file_id, user_ids=dto_request.user_ids)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")

