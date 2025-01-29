import fitz
import logging
import os

# Fonction pour extraire le texte d'un CV PDF
def extract_text_from_pdf(pdf_path, output_path):
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text() for page in doc])
        logging.info("Texte extrait du PDF avec succès.")
        
        # Écrire le texte extrait dans un fichier texte
        with open(output_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(text)
        
        return text
    except Exception as e:
        logging.error(f"Erreur lors de l'extraction du texte à partir du PDF : {e}")
        return ""

# Fonction pour parcourir les dossiers et extraire le texte de chaque PDF
def process_pdfs_in_directory(directory_path, output_base_directory):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                
                # Déterminer le chemin de sortie pour le fichier texte
                relative_path = os.path.relpath(root, directory_path)
                output_dir = os.path.join(output_base_directory, relative_path)
                os.makedirs(output_dir, exist_ok=True)
                
                output_path = os.path.join(output_dir, f"{os.path.splitext(file)[0]}.txt")
                
                extract_text_from_pdf(pdf_path, output_path)