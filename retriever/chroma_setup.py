from langchain.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from config.settings import settings

# Use local HuggingFace model for embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_chroma_db(collection_name="default"):
    db = Chroma(collection_name=collection_name, embedding_function=embeddings)
    return db 