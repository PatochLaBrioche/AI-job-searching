import requests
import logging
from src.config import CLIENT_ID, CLIENT_SECRET, SCOPES

# code INSEE de la commune (ici Toulouse)
commune = 31555
# distance en km autour de la commune
distance = 30
# grand domaine de l'offre d'emploi (ici Informatique / Télécommunication)
grandDomaine = "M18"
# motsCles nécessite une string sous la forme 'mot1,mot2,mot3'
motsCles = "développeur,html,css"
# Nature contrat
typeContrat = "CDI"
# Trie pertinence décroissante, distance croissante, date de création horodatée décroissante, origine de l'offre : sort=0 
sort = 0

# Fonction pour rechercher des offres d'emploi sur Pôle Emploi
def search_pole_emploi_jobs(keywords, access_token):
    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    job_offers = []
    for keyword in keywords:
        params = {
            'commune': commune,
            'distance': distance,
            'grandDomaine': grandDomaine,
            'motsCles': keyword,
            'typeContrat': typeContrat,
            'sort': sort
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            if response.status_code == 200:
                jobs = response.json().get('offres', [])
                job_offers.extend(jobs)
            else:
                logging.error(f"Erreur lors de la recherche sur Pôle Emploi (Code {response.status_code}): {response.text}")
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 401:
                logging.error(f"Erreur d'authentification (Code 401): {response.text}")
            else:
                logging.error(f"Erreur HTTP lors de la recherche d'offres (Code {response.status_code}): {http_err}")
        except Exception as err:
            logging.error(f"Erreur inattendue lors de la recherche d'offres : {err}")

    return job_offers
