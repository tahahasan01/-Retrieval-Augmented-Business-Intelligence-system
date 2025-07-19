import re
import string
from collections import OrderedDict
from typing import List
from sentence_transformers import SentenceTransformer, util
import nltk
from nltk.corpus import stopwords
from spellchecker import SpellChecker

# Download NLTK stopwords if not already present
try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    import nltk
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

spell = SpellChecker()
paraphrase_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(f'[{re.escape(string.punctuation)}]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def correct_spelling(text: str) -> str:
    words = text.split()
    corrected = [spell.correction(word) or word for word in words]
    return ' '.join(corrected)

def remove_stopwords(text: str) -> str:
    words = text.split()
    filtered = [w for w in words if w not in stop_words]
    return ' '.join(filtered)

def deduplicate(text: str) -> str:
    words = text.split()
    seen = OrderedDict()
    for w in words:
        if w not in seen:
            seen[w] = None
    return ' '.join(seen.keys())

def paraphrase(text: str, num_return_sequences: int = 1) -> str:
    # For demonstration, use semantic search to find the closest paraphrase in a small set
    # In production, use a true paraphrasing model or API
    # Here, just return the original text for now
    return text


def optimize_query(query: str) -> str:
    q = normalize(query)
    q = correct_spelling(q)
    q = remove_stopwords(q)
    q = deduplicate(q)
    q = paraphrase(q)
    return q 