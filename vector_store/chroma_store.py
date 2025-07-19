import chromadb
from chromadb.utils import embedding_functions

def get_or_create_collection(name):
    # Use Chroma's built-in SentenceTransformer embedding function
    hf_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    client = chromadb.Client()
    return client.get_or_create_collection(name, embedding_function=hf_ef) 