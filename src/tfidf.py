import os
import sys
import logging
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import VECTORIZER_PATH

def load_corpus():
    base_dir = 'datasets/cv_txt_processed'
    corpus = []
    filenames = []

    for root, _, files in os.walk(base_dir):
        category = os.path.basename(root)
        if category == "cv_txt_processed":
            continue

        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read().strip()
                    if text:
                        corpus.append(text)
                        filenames.append(file_path)
                except Exception as e:
                    logging.warning(f"Erreur lors de la lecture de {file_path}: {str(e)}")

    return corpus, filenames

def train_and_save_tfidf():
    corpus, filenames = load_corpus()
    
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    X = vectorizer.fit_transform(corpus)

    # Sauvegarde du modèle TF-IDF
    os.makedirs("data", exist_ok=True)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    logging.info("Vectorisation TF-IDF terminée et sauvegardée")

    return vectorizer, X, corpus, filenames

def init_vectorizer():
    if os.path.exists(VECTORIZER_PATH):
        vectorizer = joblib.load(VECTORIZER_PATH)
        logging.info("Modèle TF-IDF chargé avec succès.")
    else:
        logging.info("Modèle TF-IDF non trouvé, création en cours...")
        vectorizer, _, _, _ = train_and_save_tfidf()
        logging.info("Modèle TF-IDF créé et chargé avec succès.")
    return vectorizer

