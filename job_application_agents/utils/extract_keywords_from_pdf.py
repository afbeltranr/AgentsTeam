# utils/extract_keywords_from_pdf.py

import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_keywords(text, min_word_length=4):
    # Very simple keyword extractor: just pick "important" words
    words = re.findall(r'\b\w{%d,}\b' % min_word_length, text.lower())
    stopwords = set([
        "with", "from", "that", "this", "have", "for", "and", "the", "you", "your", 
        "are", "was", "has", "will", "can", "using", "use", "work", "skills", "experience"
    ])
    keywords = [word for word in words if word not in stopwords]
    keywords = list(set(keywords))  # Remove duplicates
    return keywords

def extract_keywords_from_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    keywords = extract_keywords(text)
    return keywords
