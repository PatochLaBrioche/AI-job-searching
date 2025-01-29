import pandas as pd
import os
import logging
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from src.txt_preprocessing import preprocess_txt_files
from sklearn.metrics import f1_score, make_scorer, hamming_loss
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import SGDClassifier

# TODO

def load_data():
    base_dir = 'datasets/cv_txt_processed'
    data_list = []

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                # Déterminer le split en fonction du dossier parent (assurez-vous que les fichiers sont bien organisés)
                split = 'train' if 'train' in root else 'val' if 'val' in root else 'test'
                
                # Ajouter le texte et son split à la liste
                data_list.append({'text': text, 'split': split})

    # Convertir en DataFrame
    return pd.DataFrame(data_list)
    

def split_data(data):
    train = data[data['split'] == 'train']
    val = data[data['split'] == 'val']
    test = data[data['split'] == 'test']
    return train, val, test

def vectorize_data(train, val, test):
    if train.empty or val.empty or test.empty:
        logging.error("One of the datasets (train, val, test) is empty.")
        return None, None, None, None
    
    logging.info(f"Training data sample: {train['text'].iloc[0]}")
    logging.info(f"Validation data sample: {val['text'].iloc[0]}")
    logging.info(f"Test data sample: {test['text'].iloc[0]}")
    
    vectorizer = TfidfVectorizer(min_df=0.00009, smooth_idf=True, tokenizer=lambda x:x.split(), sublinear_tf=False, ngram_range=(1, 3), stop_words=None)
    X_train = vectorizer.fit_transform(train['text'])
    X_val = vectorizer.transform(val['text'])
    X_test = vectorizer.transform(test['text'])
    return X_train, X_val, X_test, vectorizer

def train_classifier(X_train, y_train):
    classifier = OneVsRestClassifier(SGDClassifier(loss='log', alpha=1e-5, penalty='l1'), n_jobs=-1)
    classifier.fit(X_train, y_train)
    return classifier

def find_best_threshold(classifier, X_val, y_val):
    yhat_val_prob = classifier.predict_proba(X_val)
    best_threshold = 0.5
    best_f1_micro = 0

    for t in range(20, 31):
        threshold = t * 0.01
        pred_lb = np.asarray(yhat_val_prob > threshold, dtype='int8')
        f1_micro = f1_score(y_val, pred_lb, average='micro')
        logging.info(f"Threshold: {threshold}, Micro F1 score: {f1_micro}")
        if f1_micro > best_f1_micro:
            best_f1_micro = f1_micro
            best_threshold = threshold

    logging.info(f"Best threshold: {best_threshold}, Best Micro F1 score: {best_f1_micro}")
    return best_threshold

def evaluate_model(classifier, X_test, y_test, best_threshold):
    yhat_test_prob = classifier.predict_proba(X_test)
    pred_lb_test = np.asarray(yhat_test_prob > best_threshold, dtype='int8')

    f1_micro_test = f1_score(y_test, pred_lb_test, average='micro')
    hamming_loss_test = hamming_loss(y_test, pred_lb_test)

    logging.info(f"Micro F1 score on test data: {f1_micro_test}")
    logging.info(f"Hamming loss on test data: {hamming_loss_test}")

    return f1_micro_test, hamming_loss_test

def train_and_evaluate():
    data = load_data()
    train, val, test = split_data(data)
    X_train, X_val, X_test, vectorizer = vectorize_data(train, val, test)
    classifier = train_classifier(X_train, train['domain'])
    best_threshold = find_best_threshold(classifier, X_val, val['domain'])
    f1_micro_test, hamming_loss_test = evaluate_model(classifier, X_test, test['domain'], best_threshold)
    
    return f1_micro_test, hamming_loss_test





