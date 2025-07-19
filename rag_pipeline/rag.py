from vector_store.chroma_store import get_or_create_collection
from transformers import pipeline
import re

# Use best open-source models with fallback
try:
    summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
except Exception:
    try:
        summarizer = pipeline('summarization', model='t5-base', tokenizer='t5-base')
    except Exception:
        summarizer = pipeline('summarization', model='t5-small', tokenizer='t5-small')

try:
    qa_pipeline = pipeline('question-answering', model='deepset/deberta-v3-large-squad2')
except Exception:
    qa_pipeline = pipeline('question-answering', model='distilbert-base-uncased-distilled-squad')

def summarize_text(text, max_length=150, min_length=30):
    if len(text) > 2000:
        text = text[:2000]
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']

def hierarchical_summarize(chunks, max_length=150, min_length=30):
    chunk_summaries = [summarize_text(chunk, max_length=max_length, min_length=min_length) for chunk in chunks]
    combined = " ".join(chunk_summaries)
    return summarize_text(combined, max_length=max_length, min_length=min_length)

def extract_comparison_terms(query):
    terms = re.findall(r'Q\d+|\b20\d{2}\b|\b19\d{2}\b', query, re.IGNORECASE)
    return list(set(terms))

def rag_query(collections, query, context=None, generate_insights=False, top_k=3, summary_length='brief'):
    if context:
        if isinstance(context, dict):
            context_str = ' '.join([str(v) for v in context.values()])
        else:
            context_str = str(context)
        query = f"{context_str} {query}"
    all_docs = []
    summarize_whole = any(
        kw in query.lower() for kw in ["summarize whole", "summarize entire", "summarize all", "summarize full", "summarize complete"]
    )
    is_comparison = any(
        kw in query.lower() for kw in ["compare", "difference", "vs", "versus"]
    )
    comparison_terms = extract_comparison_terms(query) if is_comparison else []
    for collection_name in collections:
        collection = get_or_create_collection(collection_name)
        if summarize_whole:
            results = collection.get()
            docs = results['documents']
            if isinstance(docs[0], list):
                docs = [item for sublist in docs for item in sublist]
        elif is_comparison and comparison_terms:
            results = collection.get()
            docs = results['documents']
            if isinstance(docs[0], list):
                docs = [item for sublist in docs for item in sublist]
            filtered_docs = [doc for doc in docs if any(term in doc for term in comparison_terms)]
            docs = filtered_docs if filtered_docs else docs
        else:
            results = collection.query(query_texts=[query], n_results=top_k)
            docs = results['documents'][0]
        all_docs.extend(docs)
    seen = set()
    fused_docs = []
    for doc in all_docs:
        if doc not in seen:
            fused_docs.append(doc)
            seen.add(doc)
    if is_comparison:
        max_chunks = 20
        max_length = 300
        min_length = 80
    elif summary_length == 'brief':
        max_chunks = 5
        max_length = 100
        min_length = 30
    else:
        max_chunks = 15
        max_length = 250
        min_length = 80
    if generate_insights or summarize_whole or is_comparison:
        chunks_to_summarize = fused_docs[:max_chunks]
        answer = hierarchical_summarize(chunks_to_summarize, max_length=max_length, min_length=min_length)
    else:
        if fused_docs:
            context_for_qa = " ".join(fused_docs[:max_chunks])
            answer_obj = qa_pipeline(question=query, context=context_for_qa)
            answer = answer_obj['answer']
        else:
            answer = "No relevant context found."
    lineage = {"collections": collections, "context_used": bool(context), "num_docs": len(fused_docs)}
    return answer, lineage