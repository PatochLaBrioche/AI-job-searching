import pandas as pd
import os
import logging
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, hamming_loss
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import MultiLabelBinarizer

def load_data():
    base_dir = 'datasets/cv_txt_processed'
    data_list = []

    for root, _, files in os.walk(base_dir):
        category = os.path.basename(root)  # Utilisation du dossier comme label
        if category == "cv_txt_processed":  # Ignorer le dossier racine
            continue

        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read().strip()
                    
                    if not text:  # Vérifier si le fichier est vide
                        continue
                    
                    split = np.random.choice(["train", "val", "test"], p=[0.7, 0.15, 0.15])
                    data_list.append({'text': text, 'split': split, 'label': category})
                except Exception as e:
                    logging.warning(f"Erreur lors de la lecture de {file_path}: {str(e)}")

    df = pd.DataFrame(data_list)
    logging.info(f"Données chargées: {df.shape[0]} échantillons, {df['label'].nunique()} catégories")
    return df

def split_data(data):
    logging.info(f"Colonnes du dataset: {data.columns.tolist()}")
    if 'label' not in data.columns:
        raise KeyError("Le dataset est manquant la colonne 'label'")

    train = data[data['split'] == 'train']
    val = data[data['split'] == 'val']
    test = data[data['split'] == 'test']

    logging.info(f"Train: {train.shape[0]}, Val: {val.shape[0]}, Test: {test.shape[0]}")
    return train, val, test

def custom_tokenizer(text):
    return text.split()

def vectorize_data(train, val, test):
    if train.empty or val.empty or test.empty:
        raise ValueError("Un des datasets (train, val, test) est vide.")

    vectorizer = TfidfVectorizer(stop_words='english', smooth_idf=True, 
                                 tokenizer=custom_tokenizer, ngram_range=(1, 2))

    X_train = vectorizer.fit_transform(train['text'])
    X_val = vectorizer.transform(val['text'])
    X_test = vectorizer.transform(test['text'])

    logging.info("Vectorisation terminée")
    return X_train, X_val, X_test, vectorizer

def train_classifier(X_train, y_train):
    classifier = OneVsRestClassifier(SGDClassifier(loss='modified_huber', alpha=1e-5, 
                                                   penalty='l1', max_iter=1000, early_stopping=True), n_jobs=-1)
    classifier.fit(X_train, y_train)
    logging.info("Entraînement terminé")
    return classifier

def find_best_threshold(classifier, X_val, y_val):
    yhat_val_prob = classifier.predict_proba(X_val)
    best_threshold = 0.5
    best_f1_micro = 0

    for t in np.arange(0.2, 0.6, 0.05):
        pred_lb = np.asarray(yhat_val_prob > t, dtype='int8')
        f1_micro = f1_score(y_val, pred_lb, average='micro')
        if f1_micro > best_f1_micro:
            best_f1_micro = f1_micro
            best_threshold = t

    logging.info(f"Meilleur seuil trouvé: {best_threshold} avec un F1-micro de {best_f1_micro}")
    return best_threshold

def evaluate_model(classifier, X_test, y_test, best_threshold):
    predictions = classifier.predict(X_test)
    f1_micro = f1_score(y_test, predictions, average='micro')
    hamming_loss_value = hamming_loss(y_test, predictions)

    logging.info(f"Performance - F1-micro: {f1_micro}, Hamming loss: {hamming_loss_value}")
    return f1_micro, hamming_loss_value

def train_and_evaluate():
    try:
        data = load_data()
        train, val, test = split_data(data)

        X_train, X_val, X_test, vectorizer = vectorize_data(train, val, test)

        mlb = MultiLabelBinarizer()
        y_train = mlb.fit_transform(train['label'].apply(lambda x: [x]))
        y_val = mlb.transform(val['label'].apply(lambda x: [x]))
        y_test = mlb.transform(test['label'].apply(lambda x: [x]))

        classifier = train_classifier(X_train, y_train)
        best_threshold = find_best_threshold(classifier, X_val, y_val)
        evaluate_model(classifier, X_test, y_test, best_threshold)
        save_model(classifier, vectorizer, mlb)
    except Exception as e:
        logging.error(f"Une erreur est survenue: {str(e)}")
        
def save_model(classifier, vectorizer, mlb):
    os.makedirs("data", exist_ok=True)
    joblib.dump(classifier, "data/model.pkl")
    joblib.dump(vectorizer, "data/vectorizer.pkl")
    joblib.dump(mlb, "data/mlb.pkl")
    logging.info("Modèles sauvegardés dans le dossier data")
    
def load_model():
    classifier = joblib.load("data/model.pkl")
    vectorizer = joblib.load("data/vectorizer.pkl")
    mlb = joblib.load("data/mlb.pkl")
    logging.info("Modèles chargés")
    return classifier, vectorizer, mlb

def predict(text, classifier, vectorizer, mlb):
    x_new = vectorizer.transform([text])
    y_pred = classifier.predict(x_new)
    labels = mlb.inverse_transform(y_pred)    
    return labels


