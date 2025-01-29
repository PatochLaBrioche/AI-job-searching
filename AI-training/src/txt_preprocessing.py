import os
import re
import logging
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from googletrans import Translator
import asyncio

nltk.download('stopwords')
nltk.download('punkt')

stemmer_en = SnowballStemmer("english")
stemmer_fr = SnowballStemmer("french")

translator = Translator()

def preprocess_text_en(text):
    text = re.sub(r'[^A-Za-z0-9\'\-]+', ' ', text)
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    preprocessed_text = ' '.join(word for word in words if word not in stop_words and len(word) > 2)
    return preprocessed_text

def preprocess_text_fr(text):
    text = re.sub(r'[^A-Za-zÀ-ÖØ-öø-ÿ]+', ' ', text)
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('french'))
    preprocessed_text = ' '.join(word for word in words if word not in stop_words and len(word) > 2)
    return preprocessed_text

async def translate_to_french(text):
    try:
        translated = await translator.translate(text, src='en', dest='fr')
        if not translated or not translated.text.strip():
            logging.warning("Google Translate a retourné un texte vide.")
            return text  # Retourne le texte original si la traduction échoue
        return translated.text.lower()
    except Exception as e:
        logging.error(f"Erreur de traduction : {e}")
        return text  # Retourne le texte original si la traduction échoue

async def preprocess_txt_files():
    data = []
    for root, _, files in os.walk("datasets/cv_txt/"):
        for file in files:
            if file.lower().endswith('.txt'):
                txt_path = os.path.join(root, file)
                try:
                    with open(txt_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                        preprocessed_text_en = preprocess_text_en(text)
                        translated_text = await translate_to_french(preprocessed_text_en)
                        preprocessed_text_fr = preprocess_text_fr(translated_text)
                        domain = root.split(os.sep)[-1]
                        data.append({'text': preprocessed_text_fr, 'path': txt_path, 'domain': domain, 'file_name': file})
                        logging.info(f"Fichier prétraité avec succès : {txt_path} dans le dossier : {root}")
                except Exception as e:
                    logging.error(f"Erreur lors du prétraitement du fichier {txt_path} dans le dossier {root} : {e}")
                    return None
    return data

def process_and_save_txt_files():
    data = asyncio.run(preprocess_txt_files())
    for item in data:
        domain = item['domain'].split('/')[-1]  # Extract the last part of the domain path
        file_name = item['file_name']
        output_directory = f"datasets/cv_txt_processed/{domain}/"
        os.makedirs(output_directory, exist_ok=True)
        output_path = os.path.join(output_directory, file_name)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(item['text'])
            logging.info(f"Texte prétraité enregistré avec succès : {output_path}")