import re
import logging
from src.spacy_model import nlp

# Fonction pour extraire les mots-clés du CV
def extract_keywords(text):
    doc = nlp(text)
    keywords = {token.text.lower() for token in doc if token.pos_ in ["NOUN", "PROPN"] and len(token.text) > 2}
    cleaned_keywords = [kw for kw in keywords if not re.match(r'\d+', kw) and not re.match(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', kw) and not re.match(r'\d{4}', kw)]
    logging.info(f"Mots-clés extraits : {cleaned_keywords}")
    return cleaned_keywords