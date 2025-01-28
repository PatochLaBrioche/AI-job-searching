import fitz
import logging

# Fonction pour extraire le texte d'un CV PDF
def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text() for page in doc])
        logging.info("Texte extrait du PDF avec succès.")
        return text
    except Exception as e:
        logging.error(f"Erreur lors de l'extraction du texte à partir du PDF : {e}")
        return ""