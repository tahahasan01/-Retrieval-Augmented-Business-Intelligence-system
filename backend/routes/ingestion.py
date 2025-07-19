from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from ingestion.ingest_structured import ingest_csv
from ingestion.ingest_unstructured import ingest_pdf, ingest_docx, ingest_txt
import os
from fastapi.responses import JSONResponse
from ingestion.embed_documents import embed_and_store

router = APIRouter()

UPLOAD_DIR = "data/uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/ingest/structured/csv")
def upload_csv(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    df = ingest_csv(file_path)
    return {"rows": len(df), "columns": list(df.columns)}

@router.post("/ingest/unstructured/pdf")
def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    text = ingest_pdf(file_path)
    return {"chars": len(text)}

@router.post("/ingest/unstructured/docx")
def upload_docx(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    text = ingest_docx(file_path)
    return {"chars": len(text)}

@router.post("/ingest/unstructured/txt")
def upload_txt(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    text = ingest_txt(file_path)
    return {"chars": len(text)}

@router.post("/ingest_unstructured")
def ingest_unstructured(file: UploadFile = File(...), collection_name: str = Form("default")):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    ext = file.filename.lower().split(".")[-1]
    try:
        if ext == "pdf":
            text = ingest_pdf(file_path)
        elif ext == "docx":
            text = ingest_docx(file_path)
        elif ext == "txt":
            text = ingest_txt(file_path)
        elif ext == "html":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type.")
        # Chunk text before embedding
        chunk_size = 1000
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        embed_and_store(chunks, collection_name=collection_name)
        return {"filename": file.filename, "chars": len(text), "chunks": len(chunks), "collection": collection_name}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/ingested_files")
def list_ingested_files():
    try:
        files = []
        for fname in os.listdir(UPLOAD_DIR):
            fpath = os.path.join(UPLOAD_DIR, fname)
            if os.path.isfile(fpath):
                files.append([fname, str(os.path.getmtime(fpath))])
        return {"files": files}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)}) 