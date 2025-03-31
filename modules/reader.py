import os
import re
from pypdf import PdfReader

def read_pdfs_from_directory(directory_path, output_file):
    """
    Read text from all PDFs in a directory, clean it, and combine into a single corpus.
    
    :param directory_path: Path to the directory containing PDFs.
    :return: Cleaned Arabic text as a string.
    """
    corpus = ""
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory_path, filename)
            print(f"Reading {filename}...")
            text = read_pdf(file_path)
            cleaned_text = clean_text(text)
            corpus += cleaned_text + "\n"  # Separate PDFs with newlines

    # Save the cleaned corpus to a file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(corpus)
    
    print(f"Corpus saved to {output_file}")
    
    return corpus

def read_pdf(file_path):
    """
    Read text from a single PDF file.
    
    :param file_path: Path to the PDF file.
    :return: Extracted text as a string.
    """
    text = ""
    reader = PdfReader(file_path)
    for page in reader.pages:
        text += page.extract_text() or ""  # Handle empty pages
    return text

def clean_text(text):
    """
    Clean text by:
    - Removing LaTeX commands
    - Removing French (Latin script) words
    - Removing numbers and special characters
    - Keeping only valid Arabic words
    
    :param text: Raw extracted text.
    :return: Cleaned Arabic text.
    """
    # Remove LaTeX commands (e.g., \textbf{...}, \section{...})
    # text = re.sub(r'\\[a-zA-Z]+{[^}]*}', '', text)

    # Remove words with Latin characters (French, English, etc.)
    # text = re.sub(r'\b[A-Za-zÀ-ÖØ-öø-ÿ]+\b', '', text)

    # Remove numbers and special characters (except Arabic punctuation)
    # text = re.sub(r'[^ء-ي\s]', '', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def read_stop_words(file_path):
    """
    Read stop words from a file.
    
    :param file_path: Path to the stop words file.
    :return: Set of stop words.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        stop_words = set(file.read().splitlines())
    return stop_words
