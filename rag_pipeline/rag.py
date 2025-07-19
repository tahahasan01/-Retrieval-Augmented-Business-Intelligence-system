from vector_store.chroma_store import get_or_create_collection
from transformers import pipeline

# Use t5-small for summarization (already present)
summarizer = pipeline('summarization', model='t5-small', tokenizer='t5-small')
# Use distilbert-base-uncased for QA or text-generation (free, small, local)
qa_pipeline = pipeline('question-answering', model='distilbert-base-uncased-distilled-squad')
# Optionally, for text generation, use t5-small as well
# text_generator = pipeline('text2text-generation', model='t5-small')

def summarize_text(text, max_length=150, min_length=30):
    # Hugging Face pipeline expects input < 512 tokens; chunk if needed
    if len(text) > 2000:
        text = text[:2000]
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']

def rag_query(collections, query, context=None, generate_insights=False, top_k=3):
    # If context is provided, prepend it to the query
    if context:
        if isinstance(context, dict):
            context_str = ' '.join([str(v) for v in context.values()])
        else:
            context_str = str(context)
        query = f"{context_str} {query}"
    # Multi-source fusion: retrieve from all collections
    all_docs = []
    for collection_name in collections:
        collection = get_or_create_collection(collection_name)
        results = collection.query(query_texts=[query], n_results=top_k)
        docs = results['documents'][0]
        all_docs.extend(docs)
    # Deduplicate documents
    seen = set()
    fused_docs = []
    for doc in all_docs:
        if doc not in seen:
            fused_docs.append(doc)
            seen.add(doc)
    # Combine context for LLM
    combined_context = "\n".join(fused_docs)
    if generate_insights:
        answer = summarize_text(combined_context)
    else:
        # Use QA pipeline for answer generation
        if fused_docs:
            context_for_qa = " ".join(fused_docs)
            answer_obj = qa_pipeline(question=query, context=context_for_qa)
            answer = answer_obj['answer']
        else:
            answer = "No relevant context found."
    lineage = {"collections": collections, "context_used": bool(context), "num_docs": len(fused_docs)}
    return answer, lineage 