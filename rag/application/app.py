from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from rag.infrastructure.controllers import get_rag_service_aa, get_document_service
from rag.infrastructure.controllers.routers import routers

from openai import OpenAI

import os

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    openai_client = OpenAI(api_key=os.getenv("PROXYAPI_KEY"), base_url="https://api.proxyapi.ru/openai/v1")
    app.state.rag_service = get_rag_service_aa(openai_client)
    app.state.doc_service = get_document_service(openai_client)
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