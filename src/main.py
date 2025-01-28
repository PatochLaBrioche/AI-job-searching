import sys
import os
import re
import logging

# Ajouter le répertoire parent de `src` au chemin de recherche des modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.auth import get_access_token
from src.pdf_extractor import extract_text_from_pdf
from src.keyword_extractor import extract_keywords
from src.job_search import search_pole_emploi_jobs
import src.logging_config  # Pour configurer le logging

# Programme principal
if __name__ == "__main__":
    access_token = get_access_token()
    if access_token:
        print(f"Jeton d'accès obtenu : {access_token}")

        cv_path = "data/cv.pdf"
        text = extract_text_from_pdf(cv_path)
        logging.info(f"Texte extrait : {text[:200]}...")
        print(f"Texte extrait : {text[:200]}...")

        if text:
            cleaned_text = re.sub(r'\n|\r|\s+', ' ', text)
            logging.info(f"Texte nettoyé : {cleaned_text[:200]}...")
            print(f"Texte nettoyé : {cleaned_text[:200]}...")

            keywords = extract_keywords(cleaned_text)
            logging.info(f"🔎 Mots-clés détectés : {keywords}")
            print(f"🔎 Mots-clés détectés : {keywords}")

            if keywords:
                location = "Toulouse"
                job_offers = search_pole_emploi_jobs(keywords, location, access_token)

                if job_offers:
                    logging.info("\n📌 Offres trouvées :")
                    print("\n📌 Offres trouvées :")
                    for job in job_offers[:5]:
                        print(f"- {job['employeur']['nom']} | {job['intitule']} | {job['lieuTravail']['libelle']}")
                        logging.info(f"- {job['employeur']['nom']} | {job['intitule']} | {job['lieuTravail']['libelle']}")
                else:
                    logging.error("Aucune offre trouvée pour les mots-clés donnés.")
                    print("Aucune offre trouvée pour les mots-clés donnés.")
            else:
                logging.error("Aucun mot-clé trouvé dans le texte du CV.")
                print("Aucun mot-clé trouvé dans le texte du CV.")
        else:
            logging.error("Aucun texte extrait du PDF.")
            print("Aucun texte extrait du PDF.")
    else:
        logging.error("Échec de l'obtention du jeton d'accès.")
        print("Échec de l'obtention du jeton d'accès.")