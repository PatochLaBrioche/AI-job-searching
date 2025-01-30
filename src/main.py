import sys
import os
import re
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.requesting.auth import get_access_token
from src.keyword_extractor import extract_text_from_pdf, extract_keywords
from src.requesting.job_search import search_pole_emploi_jobs, save_job_offers_to_json
from src.datasets_processing.pdf_extractor import process_pdfs_in_directory
from src.datasets_processing.txt_preprocessing import process_and_save_txt_files
from src.tfidf import train_and_save_tfidf
from src.config import configure_logging, dl_nltk_packages, CV_INPUT_DATASETS_PATH, CV_OUTPUT_DATASETS_PATH, CV_INPUT_PATH

# Programme principal
if __name__ == "__main__":
    configure_logging()
    dl_nltk_packages()
    
    print("Choose an option:")
    print("1. Extrait les PDFs d'entrainement en TXTs")
    print("2. Traite et sauvegarde les TXTs nettoyés")
    print("3. Entraîne et évalue le modèle")
    print("4. Recherche des offres d'emploi correspondant à un CV")
    
    choice = input("Entrez le numéro de votre choix: ")
    
    if choice == '1':
        process_pdfs_in_directory(CV_INPUT_DATASETS_PATH, CV_OUTPUT_DATASETS_PATH)
    elif choice == '2':
        process_and_save_txt_files()
    elif choice == '3':
        train_and_save_tfidf()
    elif choice == '4':       
        access_token = get_access_token()
        if access_token:
            cv_path = CV_INPUT_PATH
            cv_text = extract_text_from_pdf()
            if cv_text:
                keywords = extract_keywords(cv_text)
                if keywords:
                    logging.info("Mots-clés extraits: " + keywords)
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
                    logging.error("Erreur durant l'extraction des mots-clés.")
            else:
                logging.error("Erreur durant l'extraction du texte du PDF.")
        else:
            logging.error("Échec de l'obtention du jeton d'accès.")
    else:
        print("Choix invalide. Veuillez entrer un nombre entre 1 et 4.")
