from langchain.chains import RetrievalQA
# from langchain.llms import OpenAI
from retriever.chroma_setup import get_chroma_db
from config.settings import settings
from rag_pipeline.rag import rag_query

# llm = OpenAI(openai_api_key=settings.openai_api_key)
# Replace with a local LLM or a placeholder function

def query_rag(query, collection):
    # Call the real RAG pipeline
    answer, lineage = rag_query([collection], query)
    return answer