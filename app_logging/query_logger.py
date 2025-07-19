import logging
from datetime import datetime

logging.basicConfig(filename='query_logs.log', level=logging.INFO)

def log_query(user: str, query: str, response: str):
    logging.info(f"{datetime.now()} | User: {user} | Query: {query} | Response: {response}") 