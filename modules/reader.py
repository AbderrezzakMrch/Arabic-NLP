import os
import re
from pypdf import PdfReader


class PDFReader:
    def read_pdfs_from_directory(self, directory_path, output_file):
        corpus = ""
        for filename in os.listdir(directory_path):
            if filename.endswith(".pdf"):
                file_path = os.path.join(directory_path, filename)
                print(f"Reading {filename}...")
                text = self.read_pdf(file_path)
                cleaned_text = self.clean_text(text)
                new_text = self.extract_arabic_words(cleaned_text)
                corpus += cleaned_text + "\n"  # Separate PDFs with newlines

        # Save the cleaned corpus to a file
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(corpus)

        print(f"Corpus saved to {output_file}")
        return corpus

    def read_pdf(self, file_path):
        text = ""
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""  # Handle empty pages
        return text

    def clean_text(self, text):
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def extract_arabic_words(self, text):
        # This regex matches Arabic words only
        arabic_words = re.findall(r'[\u0600-\u06FF]+', text)
        return arabic_words

    def read_stop_words(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            stop_words = set(file.read().splitlines())
        return stop_words
