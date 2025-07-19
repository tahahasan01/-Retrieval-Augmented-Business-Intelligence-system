from fastapi import APIRouter, Body
from ingestion.embed_documents import embed_and_store
from sentence_transformers import SentenceTransformer

router = APIRouter()

@router.post("/embed")
def embed_docs(docs: list[str] = Body(...), collection: str = Body("default")):
    db = embed_and_store(docs, collection)
    return {"status": "embedded", "collection": collection, "count": len(docs)} 