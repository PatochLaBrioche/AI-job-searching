import requests
import logging
from src.config import CLIENT_ID, CLIENT_SECRET, OAUTH_TOKEN_URL, SCOPES

# Fonction pour obtenir le jeton d'accès via OAuth2
def get_access_token():
    payload = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': SCOPES
    }

    logging.info(f"URL d'authentification : {OAUTH_TOKEN_URL}")
    logging.info(f"Payload : {payload}")

    try:
        response = requests.post(OAUTH_TOKEN_URL, data=payload)
        response.raise_for_status()
        token_info = response.json()
        access_token = token_info.get('access_token')

        if access_token:
            logging.info("Jeton d'accès obtenu avec succès.")
            return access_token
        else:
            logging.error("Jeton d'accès non trouvé dans la réponse.")
            logging.error(f"Réponse complète : {response.text}")
            return None
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"Erreur HTTP lors de l'obtention du token : {http_err}")
        logging.error(f"Réponse complète : {response.text}")
        return None
    except Exception as err:
        logging.error(f"Erreur lors de l'obtention du token : {err}")
        return None