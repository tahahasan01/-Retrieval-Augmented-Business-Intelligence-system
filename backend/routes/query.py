from fastapi import APIRouter, Body
from retriever.query_rag import query_rag

router = APIRouter()

@router.post("/query")
def query_rag_endpoint(query: str = Body(...), collection: str = Body("default")):
    answer = query_rag(query, collection)
    return {"answer": answer} 