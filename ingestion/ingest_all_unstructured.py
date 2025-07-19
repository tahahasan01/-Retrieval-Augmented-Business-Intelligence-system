import os
import subprocess
from data_ingestion.unstructured_loader import load_pdf, load_docx, load_txt, load_html
from ingestion.embed_documents import embed_and_store

# Step 1: Fetch new unstructured data from APIs
print("Fetching latest unstructured data from APIs...")
try:
    subprocess.run(["python", "ingestion/download_datasets.py"], check=True)
except Exception as e:
    print(f"download_datasets.py failed: {e}")
try:
    subprocess.run(["python", "ingestion/fetch_public_apis.py"], check=True)
except Exception as e:
    print(f"fetch_public_apis.py failed: {e}")
print("API data fetch complete. Proceeding to ingest local files.\n")

UNSTRUCTURED_DIR = 'data/unstructured/'

LOADERS = {
    '.pdf': load_pdf,
    '.docx': load_docx,
    '.txt': load_txt,
    '.html': load_html,
    '.htm': load_html,
}

CHUNK_SIZE = 2000  # characters per chunk

def ingest_all_unstructured():
    for fname in os.listdir(UNSTRUCTURED_DIR):
        fpath = os.path.join(UNSTRUCTURED_DIR, fname)
        ext = os.path.splitext(fname)[1].lower()
        loader = LOADERS.get(ext)
        if loader:
            print(f'Ingesting {fname}...')
            text = loader(fpath)
            print(f'Preview: {text[:300]}\n---\n')
            # Chunk text
            chunks = [text[i:i+CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]
            collection = os.path.splitext(fname)[0]
            embed_and_store(chunks, collection_name=collection)
            print(f'Embedded {len(chunks)} chunks from {fname} into collection {collection}.')
        else:
            print(f'Skipping {fname}: unsupported file type')

if __name__ == '__main__':
    ingest_all_unstructured()