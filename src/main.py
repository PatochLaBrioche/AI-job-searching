import sys
import os
import re
import logging

# Ajouter le répertoire parent de `src` au chemin de recherche des modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.auth import get_access_token
from src.pdf_extractor import extract_text_from_pdf
from src.keyword_extractor import extract_keywords
from src.job_search import search_pole_emploi_jobs, save_job_offers_to_json
import src.logging_config  # Pour configurer le logging

# Programme principal
if __name__ == "__main__":
    access_token = get_access_token()
    if access_token:
        logging.info(f"Jeton d'accès obtenu : {access_token}")

        cv_path = "data/cv.pdf"
        text = extract_text_from_pdf(cv_path)

        if text:
            cleaned_text = re.sub(r'\n|\r|\s+', ' ', text)
            keywords = extract_keywords(cleaned_text)

            if keywords:
                job_offers = search_pole_emploi_jobs(keywords, access_token)
                
                # Créer le répertoire /data s'il n'existe pas
                os.makedirs('data', exist_ok=True)
                
                # Enregistrer les résultats dans un fichier JSON
                if job_offers:
                    save_job_offers_to_json(job_offers, 'data/job_offers.json')
                    logging.info("Offres trouvées et enregistrées dans 'data/job_offers.json'.")
                else:
                    if os.path.exists('data/job_offers.json'):
                        os.remove('data/job_offers.json')
                    logging.error("Aucune offre trouvée pour les mots-clés donnés.")
            else:
                logging.error("Aucun mot-clé trouvé dans le texte du CV.")
        else:
            logging.error("Aucun texte extrait du PDF.")
    else:
        logging.error("Échec de l'obtention du jeton d'accès.")
