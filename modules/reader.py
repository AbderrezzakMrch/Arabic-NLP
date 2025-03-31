# modules/reader.py
from pypdf import PdfReader
import os

def read_pdf(file_path):
    """
    Read text from a PDF file.

    :param file_path: Path to the PDF file.
    :return: Extracted text as a string.
    """
    text = ""
    reader = PdfReader(file_path)
    for page in reader.pages:
        text += page.extract_text()
    return text


def read_pdfs_from_directory(directory_path, output_file):
    """
    Read text from all PDFs in a directory and save the combined text to a file.

    :param directory_path: Path to the directory containing PDFs.
    :param output_file: Path to save the combined text.
    """
    corpus = ""
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory_path, filename)
            print(f"Reading {filename}...")
            corpus += read_pdf(file_path)

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(corpus)
    print(f"Combined text saved to {output_file}")