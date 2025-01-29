import os
import requests
import logging
import json
from src.config import CLIENT_ID, CLIENT_SECRET, SCOPES

# code INSEE de la commune (ici Toulouse)
commune = 31555
# distance en km autour de la commune
distance = 30
# grand domaine de l'offre d'emploi (ici Informatique / Télécommunication)
grandDomaine = "M18"
# motsCles nécessite une string sous la forme 'mot1,mot2,mot3'
motsCles = "developpeur,web,fullstack,php"
# Nature contrat
typeContrat = "CDI"
# Trie pertinence décroissante, distance croissante, date de création horodatée décroissante, origine de l'offre : sort=0 
sort = 0

# Fonction pour rechercher des offres d'emploi sur Pôle Emploi
def search_pole_emploi_jobs(keywords, access_token):
    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    all_results = []
    seen_ids = set()
    # Remplacer motsCles par la liste en paramètre quand fonctionnel
    for keyword in motsCles.split(','):
        params = {
            "commune": commune,
            "distance": distance,
            "grandDomaine": grandDomaine,
            "motsCles": keyword,
            "typeContrat": typeContrat,
            "sort": sort
        }
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            for offer in response.json().get('resultats', []):
                if offer['id'] not in seen_ids:
                    seen_ids.add(offer['id'])
                    all_results.append(offer)
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 401:
                logging.error(f"Erreur d'authentification (Code 401): {response.text}")
            else:
                logging.error(f"Erreur HTTP lors de la recherche d'offres (Code {response.status_code}): {http_err}")
        except Exception as err:
            logging.error(f"Erreur inattendue lors de la recherche d'offres : {err}")

    logging.info(f"{len(all_results)} offres trouvées pour les mots-clés suivants : {motsCles}")
    return all_results

# Fonction pour supprimer les clés indésirables des résultats
def remove_unwanted_keys(job_offers):
    keys_to_remove = [
        "romeCode", "romeLibelle", "appellationlibelle", "typeContratLibelle",
        "natureContrat", "experienceExige", "alternance", "accessibleTH",
        "qualificationCode", "qualificationLibelle", "codeNAF", "secteurActivite",
        "offresManqueCandidats"
    ]
    for offer in job_offers:
        for key in keys_to_remove:
            if key in offer:
                del offer[key]
    return job_offers

# Fonction pour enregistrer les résultats dans un fichier JSON
def save_job_offers_to_json(job_offers, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(job_offers, f, ensure_ascii=False, indent=4)

# Exemple d'utilisation
if __name__ == "__main__":
    access_token = "votre_access_token"
    results = search_pole_emploi_jobs(motsCles, access_token)
    cleaned_results = remove_unwanted_keys(results)
    save_job_offers_to_json(cleaned_results, "job_offers.json")
    print("Les résultats ont été enregistrés dans job_offers.json")