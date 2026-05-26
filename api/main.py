from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import StreamingResponse
from typing import Annotated
from pydantic import BaseModel
import logging
import time
import os
from api.deps import retriever
from api.rag import ask as rag_ask
from api.cache import check_rate_limit
from core import chunk_text
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY", "dev-key-123")


async def verify_api_key(x_api_key: Annotated[str, Header()]):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API Key اشتباه است")


app = FastAPI(title="Persian RAG Starter", version="1.0.0")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    logger.info(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} "
        f"duration={duration:.3f}s"
    )
    return response


class QueryRequest(BaseModel):
    query: str


class AddRequest(BaseModel):
    text: str
    doc_id: str


@app.get("/")
async def root():
    return {"name": "Persian RAG Starter", "version": "1.0.0"}


@app.post("/add")
async def add(request: AddRequest, x_api_key: Annotated[str, Header()]):
    await verify_api_key(x_api_key)
    chunks = chunk_text(request.text)
    retriever.add(chunks, ids=[f"{request.doc_id}_chunk_{i}" for i in range(len(chunks))])
    return "done"


@app.post("/ask")
async def ask(request: QueryRequest, x_api_key: Annotated[str, Header()]):
    await verify_api_key(x_api_key)
    if not check_rate_limit(x_api_key):
        raise HTTPException(status_code=429, detail="تعداد درخواست زیاد است، کمی صبر کنید")
    generator = await rag_ask(request.query)
    return StreamingResponse(generator(), media_type="text/plain")
