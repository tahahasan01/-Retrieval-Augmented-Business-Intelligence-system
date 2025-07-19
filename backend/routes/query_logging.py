from fastapi import APIRouter, Depends, HTTPException
from app_logging.query_logger import log_query
import os
from typing import List
from datetime import datetime

router = APIRouter()

# In-memory query log for analytics (for demo; use DB in production)
QUERY_LOG = []

@router.post("/log_query")
def log_query_route(user: str, query: str, response: str):
    log_query(user, query, response)
    QUERY_LOG.append({
        "user": user,
        "query": query,
        "response": response,
        "timestamp": datetime.utcnow().isoformat()
    })
    return {"status": "logged"}

@router.get("/analytics")
def get_analytics():
    return {
        "total_queries": len(QUERY_LOG),
        "recent_queries": QUERY_LOG[-10:]
    }

@router.get("/logs")
def get_logs():
    log_file = "query_logs.log"
    if not os.path.exists(log_file):
        raise HTTPException(status_code=404, detail="Log file not found")
    with open(log_file, "r") as f:
        logs = f.read()
    return {"logs": logs} 