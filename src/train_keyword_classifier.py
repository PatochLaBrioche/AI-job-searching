import os
import sys
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils.class_weight import compute_class_weight
import json

def load_annotated_data_json(file_path):
    """
    Charge les données annotées à partir d'un fichier JSON.

    :param file_path: Chemin vers le fichier JSON.
    :return: Tuple contenant les mots-clés et les étiquettes.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print(f"Data loaded: {data}")  # Ajout d'une impression pour vérifier les données chargées
            keywords = [item['keyword'] for item in data]
            labels = [item['label'] for item in data]
            return keywords, labels
    except FileNotFoundError:
        print(f"Le fichier {file_path} n'a pas été trouvé.")
    except json.JSONDecodeError:
        print(f"Erreur de décodage JSON dans le fichier {file_path}.")
    except KeyError as e:
        print(f"Clé manquante dans les données JSON : {e}")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
    return [], []

# Entraîner un classifieur de mots-clés à partir du dataset JSON
def train_keyword_classifier_from_json(json_path, vectorizer_path, model_path):
    """
    Entraîne un modèle supervisé pour classifier les mots-clés pertinents et non pertinents.
    """

    # Charger les données annotées depuis le JSON
    keywords, labels = load_annotated_data_json(json_path)

    # Charger ou créer le vectorizer
    if os.path.exists(vectorizer_path):
        vectorizer = joblib.load(vectorizer_path)
        X = vectorizer.transform(keywords)
    else:
        vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        X = vectorizer.fit_transform(keywords)

    # Calculer les poids des classes
    class_weights = compute_class_weight('balanced', classes=np.unique(labels), y=labels)
    class_weights_dict = {i: class_weights[i] for i in range(len(class_weights))}

    # Charger ou créer le modèle
    if os.path.exists(model_path):
        model = joblib.load(model_path)
    else:
        model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight=class_weights_dict)

    # Séparer en données d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

    # Entraîner le modèle
    model.fit(X_train, y_train)

    # Évaluer le modèle
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    # Sauvegarder le modèle et le vectorizer
    joblib.dump(vectorizer, vectorizer_path)
    joblib.dump(model, model_path)
    print("Modèle et vectorizer sauvegardés.")

def train_keyword_classifier(data, vectorizer_path, model_path):
    """
    Entraîne un modèle supervisé pour classifier les mots-clés pertinents et non pertinents en utilisant les données fournies.
    """
    keywords, labels = data

    # Charger ou créer le vectorizer
    if os.path.exists(vectorizer_path):
        vectorizer = joblib.load(vectorizer_path)
        X = vectorizer.transform(keywords)
    else:
        vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        X = vectorizer.fit_transform(keywords)

    # Calculer les poids des classes
    class_weights = compute_class_weight('balanced', classes=np.unique(labels), y=labels)
    class_weights_dict = {i: class_weights[i] for i in range(len(class_weights))}

    # Charger ou créer le modèle
    if os.path.exists(model_path):
        model = joblib.load(model_path)
    else:
        model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight=class_weights_dict)

    # Séparer en données d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

    # Entraîner le modèle
    model.fit(X_train, y_train)

    # Évaluer le modèle
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    # Sauvegarder le modèle et le vectorizer
    joblib.dump(vectorizer, vectorizer_path)
    joblib.dump(model, model_path)
    print("Modèle et vectorizer sauvegardés.")

if __name__ == "__main__":
    
    # Exemple d'utilisation
    file_path = 'datasets/resume_corpus_dataset/Anant_Kedia_export_41156_project.json'
    data = load_annotated_data_json(file_path)
    if data:
        vectorizer_path = "data/keyword_vectorizer.pkl"
        model_path = "data/keyword_classifier.pkl"

        # Modification pour utiliser les données récupérées
        train_keyword_classifier(data, vectorizer_path, model_path)
