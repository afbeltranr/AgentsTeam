# utils/extract_keywords_from_pdf.py

import fitz  # PyMuPDF
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

def extract_keywords_from_pdf(pdf_path, top_k=10):
    # 1. Extract text from PDF
    with fitz.open(pdf_path) as doc:
        text = " ".join([page.get_text() for page in doc])

    # 2. Preprocess text
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = word_tokenize(text)
    words = [word for word in words if word not in stopwords.words('english') and len(word) > 2]

    # 3. Apply TF-IDF (yes, on a single document — for term frequency)
    cleaned_text = " ".join(words)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([cleaned_text])
    tfidf_scores = zip(vectorizer.get_feature_names_out(), tfidf_matrix.toarray()[0])
    
    # 4. Sort by relevance
    ranked_keywords = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)

    # 5. (Optional) Boost priority terms
    priority_terms = ['python', 'data', 'analysis', 'sql', 'machine', 'learning', 'visualization']
    boosted = []
    for word, score in ranked_keywords:
        if word in priority_terms:
            boosted.append((word, score + 1.0))  # Boost important keywords
        else:
            boosted.append((word, score))

    # 6. Return top-k keywords
    final_keywords = sorted(boosted, key=lambda x: x[1], reverse=True)
    return [word for word, _ in final_keywords[:top_k]]
