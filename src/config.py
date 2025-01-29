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

# Charger le modèle de langue spaCy
nlp = spacy.load("fr_core_news_md")

# Configure logging
os.makedirs("logs", exist_ok=True)
with open('logs/logs.log', 'w', encoding='utf-8'):
    pass
logging.basicConfig(
    level=logging.INFO,
    filename="logs/logs.log",
    filemode="w",
    format="%(asctime)s - %(message)s",
    encoding="utf-8"
)