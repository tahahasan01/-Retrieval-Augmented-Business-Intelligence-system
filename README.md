# RAG Intelligence System

A full-stack, production-ready Retrieval-Augmented Generation (RAG) Intelligence System for business analytics, document Q&A, and automated insight generation using only local models and embeddings.

---

## 🚀 Overview

RAG Intelligence System enables you to:
- Ingest and analyze both structured (CSV) and unstructured (PDF, DOCX, TXT, HTML) data
- Ask natural language questions and get context-aware, explainable answers
- Generate summaries, insights, and comparisons from your data
- Use only local LLMs and embeddings (no OpenAI API required)
- Run everything locally or in Docker
- Enjoy a modern, dark-themed Streamlit dashboard

---

## ✨ Features
- **RAG Pipeline:** Multi-source retrieval, context-aware query optimization, hierarchical summarization, and lineage tracking
- **Local Embeddings & LLMs:** HuggingFace Sentence Transformers, T5, and DistilBERT
- **Structured & Unstructured Data:** Batch and manual ingestion, file upload UI, analytics
- **Advanced Querying:** Summarization, comparison, insight generation, and more
- **Production Backend:** FastAPI, JWT auth, logging, error handling, monitoring
- **Modern Frontend:** Streamlit app with query, analytics, ingestion, and debug tools
- **Deployment Ready:** Docker support, easy local and cloud deployment

---

## 🛠️ Tech Stack
- **Backend:** FastAPI, Uvicorn, ChromaDB, SQLAlchemy, Pydantic, JWT, LangChain, HuggingFace Transformers
- **Frontend:** Streamlit (Python)
- **AI/ML:** Sentence Transformers, T5, DistilBERT (all local)
- **Vector Store:** ChromaDB
- **Containerization:** Docker, docker-compose

---

## ⚡ Quickstart

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/rag-intelligence-system.git
cd rag-intelligence-system
```

### 2. Install Python Dependencies
```bash
pip install -r backend/requirements.txt
pip install streamlit
```

### 3. Run Backend (FastAPI)
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Run Frontend (Streamlit)
```bash
streamlit run streamlit_app.py
```

### 5. (Optional) Run with Docker
```bash
docker-compose up --build
```

---

## 📂 Project Structure
```
RAG_intelligence_System/
├── api/                  # FastAPI entrypoint
├── backend/              # Backend app, routes, services
├── config/               # Config files
├── data/                 # Structured & unstructured data
├── data_ingestion/       # Data loaders
├── ingestion/            # Ingestion scripts
├── logging/              # Query logging
├── rag_pipeline/         # RAG logic
├── retriever/            # ChromaDB setup, query logic
├── vector_store/         # ChromaDB vector store
├── streamlit_app.py      # Streamlit frontend
├── docker-compose.yml    # Docker config
└── README.md             # This file
```

---

## 🧑‍💻 Usage

### Ingest Data
- **Batch ingest:** Use the Streamlit UI or run `python ingestion/ingest_all_structured.py` and `python ingestion/ingest_all_unstructured.py` to process all files in `data/structured` and `data/unstructured`.
- **Manual upload:** Use the Streamlit UI to upload new CSV, PDF, DOCX, TXT, or HTML files.

### Query Data
- Ask natural language questions in the Streamlit UI.
- Use options for query optimization, insight generation, and summary length.
- Compare, summarize, or extract insights from your data.

### Analytics & Debug
- View query history and analytics in the UI.
- Use debug tools to inspect ingested documents and collections.

---

## 🏗️ Deployment

### Local
- Run backend and frontend as described above.

### Docker
- Build and run with `docker-compose up --build`.
- Exposes backend on port 8000 and Streamlit UI on port 8501.

### Cloud
- Backend can be deployed to Render, Railway, or similar.
- Streamlit frontend can be deployed to Streamlit Cloud or similar.

---

## 🔒 Authentication
- JWT-based authentication is available (see `backend/routes/auth.py`).
- For demo, default credentials are used. Update for production.

---

## 📝 Customization
- Add your own datasets to `data/structured` or `data/unstructured` and re-ingest.
- Swap in larger local models for better summarization (see `rag_pipeline/rag.py`).
- Extend Streamlit UI for more analytics or user management.

---

## 🤝 Contributing
Pull requests and issues welcome! Please open an issue to discuss major changes.

---

## 📄 License
MIT License
