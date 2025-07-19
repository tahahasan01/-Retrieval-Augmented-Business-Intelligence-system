from fastapi import FastAPI
from backend.routes import ingestion, embed, query, auth, query_logging as log_routes
from pydantic import BaseModel
from fastapi import Depends
from backend.utils.auth import verify_token
from rag_pipeline.rag import rag_query
from app_logging.query_logger import log_query
from backend.utils.query_optimizer import optimize_query
from fastapi.responses import JSONResponse
from fastapi import Request
from vector_store.chroma_store import get_or_create_collection

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(ingestion.router, prefix="/ingestion", tags=["ingestion"])
app.include_router(embed.router, tags=["embedding"])
app.include_router(query.router, tags=["query"])
app.include_router(log_routes.router, tags=["logging"])

class QueryRequest(BaseModel):
    query: str
    collection: str
    optimize_query: bool = False  # Enable query optimization
    context: dict = None          # User/session context for context-aware responses
    sources: list = None          # List of collections/sources for multi-source fusion
    generate_insights: bool = False  # Enable automated insight generation

@app.get("/")
def read_root():
    return {"message": "RAG Business Intelligence API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/query")
def query_rag(request: QueryRequest, user=Depends(verify_token)):
    try:
        # Query optimization (advanced)
        query_text = request.query
        if request.optimize_query:
            query_text = optimize_query(query_text)
        # Multi-source fusion: use provided sources or default to single collection
        collections = request.sources if request.sources else [request.collection]
        # Context-aware: pass context if provided
        response, lineage = rag_query(
            collections=collections,
            query=query_text,
            context=request.context,
            generate_insights=request.generate_insights
        )
        # Log query for analytics
        from backend.routes.query_logging import log_query_route
        log_query_route(user.get("sub", "unknown"), query_text, response)
        return {"answer": response, "lineage": lineage}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/debug/list_documents")
def list_documents(collection: str = "default"):
    try:
        col = get_or_create_collection(collection)
        # ChromaDB returns documents in 'documents' field
        results = col.get()
        docs = results.get('documents', [])
        return {"collection": collection, "num_documents": len(docs), "documents": docs}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)}) 