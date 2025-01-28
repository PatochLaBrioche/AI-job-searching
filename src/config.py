import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les clés API depuis les variables d'environnement
CLIENT_ID = os.getenv("POLE_EMPLOI_CLIENT_ID")
CLIENT_SECRET = os.getenv("POLE_EMPLOI_SECRET_KEY")
OAUTH_TOKEN_URL = "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=/partenaire"
SCOPES = "api_offresdemploiv2 o2dsoffre"