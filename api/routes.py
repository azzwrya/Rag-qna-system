from fastapi import APIRouter, UploadFile, BackgroundTasks, Request
import shutil
from pydantic import BaseModel

from api.limiter import limiter
from background_jobs.ingestion import process_document
from vector_store.faiss_store import search_index
from api.gemini_utils import generate_answer

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile, background_tasks: BackgroundTasks):
    file_location = f"data/uploads/{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    background_tasks.add_task(process_document, file_location)

    return {
        "message": f"File '{file.filename}' uploaded. Processing in background."
    }


class QueryRequest(BaseModel):
    question: str


@router.post("/ask")
@limiter.limit("5/minute")
async def ask_question(request: Request, request_data: QueryRequest):
    # 🔍 Get chunks AND distance scores
    chunks, scores = search_index(request_data.question, k=3)

    if not chunks:
        return {"answer": "No documents found."}

    # 🤖 Generate answer using retrieved chunks
    answer = generate_answer(request_data.question, chunks)

    # 📊 Return answer + retrieval metrics
    return {
        "question": request_data.question,
        "answer": answer,
        "metrics": {
            "top_k_distances": scores,
            "average_distance": sum(scores) / len(scores) if scores else 0
        },
        "sources": chunks
    }
