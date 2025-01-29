import os
import sys
import logging
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pdf_extractor import process_pdfs_in_directory
from src.txt_preprocessing import process_and_save_txt_files
from src.tfidf import train_and_evaluate

def dl_nltk_packages():
    import nltk
    nltk.download('stopwords')
    nltk.download('punkt')
    
# Configure logging
os.makedirs("logs", exist_ok=True)
with open('logs/logs.log', 'w', encoding='utf-8'):
    pass
logging.basicConfig(
    level=logging.INFO,
    filename="logs/logs.log",
    filemode="w",
    format="%(asctime)s - %(message)s",
    encoding="utf-8"
)

def extract_text_from_pdf():    
    base_directory = "datasets/cv_pdf/"
    output_base_directory = "datasets/cv_txt/"
    process_pdfs_in_directory(base_directory, output_base_directory)
    
# Programme principal
if __name__ == "__main__":
    # prompt to user to let him chose what to do
    dl_nltk_packages()
    print("Choose an option:")
    print("1. Extract PDFs into TXTs")
    print("2. Process and save text files")
    print("3. Train and evaluate")
    
    choice = input("Enter the number of your choice: ")
    
    if choice == '1':
        extract_text_from_pdf()
    elif choice == '2':
        process_and_save_txt_files()
    elif choice == '3':
        train_and_evaluate()
    else:
        print("Invalid choice. Please enter a number between 1 and 3.")