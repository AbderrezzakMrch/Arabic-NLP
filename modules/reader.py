import os
from pypdf import PdfReader
import re

class PDFReader:
    def read_pdfs_from_directory(self, directory_path, output_file):
        """Read all PDFs while cleaning extra spaces but keeping documents separated"""
        corpus_parts = []

        try:
            for filename in sorted(os.listdir(directory_path)):
                if filename.endswith(".pdf"):
                    file_path = os.path.join(directory_path, filename)
                    print(f"Processing {filename}...")

                    try:
                        text = self.read_pdf(file_path)
                        if text:
                            corpus_parts.append(text)
                    except Exception as e:
                        print(f"Skipped {filename} (error: {str(e)})")
                        continue

        except Exception as e:
            print(f"Directory reading failed: {str(e)}")
            return ""

        # Join with double newlines between documents
        full_corpus = "\n\n".join(corpus_parts)

        # Save to file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(full_corpus)

        print(f"Created cleaned corpus at {output_file}")
        return full_corpus

    def read_pdf(self, file_path):
        """Read a PDF with internal space normalization"""
        text_lines = []
        reader = PdfReader(file_path)

        for page in reader.pages:
            try:
                page_text = page.extract_text()
                if page_text:
                    # Clean spaces but preserve paragraph structure
                    cleaned_page = self._clean_spaces(page_text)
                    text_lines.append(cleaned_page)
            except Exception:
                continue  # Skip problematic pages

        # Join pages with single newlines (preserves original paragraphs)
        return "\n".join(text_lines)

    def _clean_spaces(self, text):
        """Normalize spaces while preserving structure"""
        # Replace all whitespace sequences with single space
        text = re.sub(r'\s+', ' ', text.strip())

        text = re.sub(r'([^\n])\s+([\u0600-\u06FF]{2,})', r'\1 \2', text)  # Clean Arabic spacing

        return text.strip()


    def normalize_arabic(self,text):
        text = re.sub(r'[ًٌٍَُِّْـ]', '', text)  # Remove Tashkeel
        """
        text = re.sub(r'[إأآا]', 'ا', text)  # Normalize Alif
        text = re.sub(r'ى', 'ي', text)  # Normalize Alef Maqsura
        text = re.sub(r'ؤ', 'و', text)  # Normalize Waw with Hamza
        text = re.sub(r'ئ', 'ي', text)  # Normalize Yeh with Hamza
        text = re.sub(r'ة', 'ه', text)  # Normalize Teh Marbuta
        """
        return text

    def read_stop_words(self, file_path):
        """Read and normalize stop words file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return set(self.normalize_arabic(line.strip()) for line in f if line.strip())
        except Exception as e:
            print(f"Error reading stop words file: {str(e)}")
            return set()

    def read_dictionary(self):
        """Read and normalize dictionary files"""
        dictionary_words = set()
        dictionary_files = [
            "data/ArabicDictionary/adhesiontext Arabic Dictionary.txt",
            "data/ArabicDictionary/arabic_dict.txt",
            "data/ArabicDictionary/Clean_tokens.txt",
            "data/ArabicDictionary/DictArabe1.txt",
            "data/ArabicDictionary/DictArabe3.txt",
            "data/ArabicDictionary/DictArabe4.txt"
        ]

        for dict_file in dictionary_files:
            try:
                for encoding in ['utf-8', 'windows-1256', 'iso-8859-6']:
                    try:
                        with open(dict_file, 'r', encoding=encoding) as f:
                            dictionary_words.update(
                                self.normalize_arabic(line.strip()) for line in f if line.strip()
                            )
                        break
                    except UnicodeDecodeError:
                        continue
            except Exception as e:
                print(f"Error loading dictionary {dict_file}: {str(e)}")

        return dictionary_words
