import re
import logging
import fitz
from src.config import CV_INPUT_PATH
from src.tfidf import load_model, predict


def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text() for page in doc])
        logging.info("Texte extrait du PDF avec succès.")
        return text
    except Exception as e:
        logging.error(f"Erreur lors de l'extraction du texte à partir du PDF : {e}")
        return ""
    
# Fonction pour extraire les mots-clés du CV
def extract_keywords(text):
    classifier, vectorizer, mlb = load_model()
    keywords = predict(text, classifier, vectorizer, mlb)
    logging.info(f"Mots-clés extraits: {keywords}")
    return keywords