import os
import pandas as pd
from .embed_documents import embed_and_store

RAW_STRUCTURED_DIR = 'data/raw/structured/'

for fname in os.listdir(RAW_STRUCTURED_DIR):
    if fname.endswith('.csv'):
        path = os.path.join(RAW_STRUCTURED_DIR, fname)
        print(f'Processing {fname}...')
        df = pd.read_csv(path)
        # Chunking: convert each row to a string (customize as needed)
        docs = [str(row.to_dict()) for _, row in df.iterrows()]
        collection = fname.replace('.csv', '')
        embed_and_store(docs, collection_name=collection)
        print(f'Embedded {len(docs)} rows from {fname} into collection {collection}.') 