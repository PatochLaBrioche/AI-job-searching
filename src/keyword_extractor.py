import re
import logging
import fitz
import numpy as np
from src.config import CV_INPUT_PATH
from src.tfidf import init_vectorizer


def extract_text_from_pdf():
    try:
        doc = fitz.open(CV_INPUT_PATH)
        text = "\n".join([page.get_text() for page in doc])
        logging.info("Texte extrait du PDF avec succès.")
        return text
    except Exception as e:
        logging.error(f"Erreur lors de l'extraction du texte à partir du PDF : {e}")
        return ""

def extract_keywords(text, top_n=10):
    vectorizer = init_vectorizer()
    
    # Transformer le texte
    X_new = vectorizer.transform([text])
    
    # Obtenir les scores TF-IDF
    feature_names = np.array(vectorizer.get_feature_names_out())
    scores = X_new.toarray().flatten()
    
    # Trier et sélectionner les meilleurs mots-clés
    top_indices = np.argsort(scores)[::-1][:top_n]
    keywords = feature_names[top_indices]
    
    keywords = ','.join(keywords)
    return keywords
