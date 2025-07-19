import pdfplumber
from docx import Document
from typing import List
from bs4 import BeautifulSoup

def load_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def load_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def load_txt(file_path: str) -> str:
    """Load text from a TXT file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def load_html(file_path: str) -> str:
    """Extract text from an HTML file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        return soup.get_text(separator=' ', strip=True) 