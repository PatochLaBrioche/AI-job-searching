import requests
import logging

# Fonction pour rechercher des offres d'emploi sur Pôle Emploi
def search_pole_emploi_jobs(keywords, location, access_token):
    url = "https://api.francetravail.io/partenaire/offresdemploi"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    job_offers = []
    for keyword in keywords:
        params = {
            'q': keyword,
            'l': location,
            'distance': '50',
            'limit': 5,
        }
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            if response.status_code == 200:
                jobs = response.json().get('offres', [])
                job_offers.extend(jobs)
            else:
                logging.error(f"Erreur lors de la recherche sur Pôle Emploi (Code {response.status_code}): {response.text}")
                print(f"Erreur {response.status_code} : {response.text}")
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 401:
                logging.error(f"Erreur d'authentification (Code 401): {response.text}")
            else:
                logging.error(f"Erreur HTTP lors de la recherche d'offres (Code {response.status_code}): {http_err}")
        except Exception as err:
            logging.error(f"Erreur inattendue lors de la recherche d'offres : {err}")

    return job_offers