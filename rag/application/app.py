from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from rag.infrastructure.controllers import get_rag_service_aa
from rag.infrastructure.controllers.routers import routers

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    _ = get_rag_service_aa()
    yield


app = FastAPI(title="RAG API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in routers:
    app.include_router(router)


@app.exception_handler(Exception)
async def custom_exception_handler(_: Request, exception: Exception):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": str(exception)})

if __name__ == "__main__":
    uvicorn.run(app="rag.application.app:app", host="0.0.0.0", port=8000, reload=True)