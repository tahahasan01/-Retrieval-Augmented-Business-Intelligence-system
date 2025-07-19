import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from langchain_community.embeddings import HuggingFaceEmbeddings

# Initialize Chroma client
client = chromadb.Client(Settings())

# Use OpenAI embedding function (or replace with another)
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key="YOUR_OPENAI_API_KEY", # Replace with your key or use env var
    model_name="text-embedding-ada-002"
)

def get_or_create_collection(name):
    # Use HuggingFace embedding function for local embeddings
    hf_ef = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    client = chromadb.Client()  # Use the correct Chroma client
    return client.get_or_create_collection(name, embedding_function=hf_ef) 