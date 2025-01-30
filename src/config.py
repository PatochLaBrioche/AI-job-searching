import os
import spacy
import logging
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les clés API depuis les variables d'environnement
CLIENT_ID = os.getenv("POLE_EMPLOI_CLIENT_ID")
CLIENT_SECRET = os.getenv("POLE_EMPLOI_SECRET_KEY")
OAUTH_TOKEN_URL = "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=/partenaire"
SCOPES = "api_offresdemploiv2 o2dsoffre"
CV_INPUT_PATH = "data/cv.pdf"
CV_INPUT_DATASETS_PATH = "datasets/cv_pdf/"
CV_OUTPUT_DATASETS_PATH = "datasets/cv_txt/"
VECTORIZER_PATH = "data/tfidf_vectorizer.pkl"

# Charger le modèle de langue spaCy
nlp = spacy.load("fr_core_news_md")

def configure_logging():
    # Configure logging
    os.makedirs("logs", exist_ok=True)
    with open('logs/logs.log', 'w', encoding='utf-8'):
        pass
    logging.basicConfig(
        level=logging.INFO,
        filename="logs/logs.log",
        filemode="w",
        format="%(asctime)s - %(filename)s - %(lineno)d - %(message)s",
        encoding="utf-8"
    )
    
def dl_nltk_packages():
    import nltk
    nltk.download('stopwords')
    nltk.download('punkt')