import joblib
import sys
import os
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                
from src.tfidf import init_vectorizer

# Charger le modèle entraîné
vectorizer = joblib.load("data/keyword_vectorizer.pkl")
model = joblib.load("data/keyword_classifier.pkl")

def filter_keywords(keywords):
    """
    Filtre les mots-clés en utilisant le classifieur.
    Retourne uniquement les mots-clés jugés pertinents.
    """
    X = vectorizer.transform(keywords)
    predictions = model.predict(X)

    # Sélectionner uniquement les mots-clés classés comme "pertinents"
    relevant_keywords = [kw for kw, label in zip(keywords, predictions) if label == 1]

    return relevant_keywords

# Exemple d'utilisation
if __name__ == "__main__":
    extracted_keywords = ["développement web", "stage", "compétences techniques", "Python", "machine learning"]
    filtered_keywords = filter_keywords(extracted_keywords)
    print("Mots-clés filtrés :", filtered_keywords)
