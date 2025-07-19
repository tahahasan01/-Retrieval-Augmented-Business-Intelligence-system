from data_ingestion.unstructured_loader import load_pdf, load_docx, load_txt

def ingest_pdf(file_path: str):
    return load_pdf(file_path)

def ingest_docx(file_path: str):
    return load_docx(file_path)

def ingest_txt(file_path: str):
    return load_txt(file_path) 