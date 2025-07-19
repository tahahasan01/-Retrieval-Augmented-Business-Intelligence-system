from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from config.settings import settings
from app_logging.query_logger import log_query

# Example function to embed and store documents

def embed_and_store(docs, collection_name="default"):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(collection_name=collection_name, embedding_function=embeddings)
    db.add_texts(docs)
    return db