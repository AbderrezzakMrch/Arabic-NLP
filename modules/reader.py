import os
import re
from pypdf import PdfReader


class PDFReader:
    def read_pdfs_from_directory(self, directory_path, output_file):
        corpus = ""
        try:
            for filename in os.listdir(directory_path):  # list of directory
                if filename.endswith(".pdf"):  # just li ficher li ykmlo bl pdf
                    file_path = os.path.join(directory_path, filename)  # path + file name
                    print(f"Reading {filename}...")
                    try:
                        text = self.read_pdf(file_path)
                        cleaned_text = self.clean_text(text)
                        corpus += cleaned_text + "\n"  # Separate PDFs with newlines
                    except Exception as e:
                        print(f"Error processing file {filename}: {str(e)}")
                        continue

            # Save the cleaned corpus to a file
            try:
                with open(output_file, "w", encoding="utf-8") as file:
                    file.write(corpus)
                print(f"Corpus saved to {output_file}")
            except Exception as e:
                print(f"Error saving corpus to {output_file}: {str(e)}")

        except Exception as e:
            print(f"Error reading directory {directory_path}: {str(e)}")
            return ""

        return corpus

    def clean_token(self, token):
        """Extract clean Arabic words as separate tokens."""
        return re.findall(r'[\u0621-\u063A\u0641-\u064A]{2,}', token)
    def read_pdf(self, file_path):
        text = ""
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                try:
                    text += " ".join(self.clean_token(page.extract_text()) or [])  # Cleaned Arabic tokens and Handle empty pages
                except Exception as e:
                    print(f"Error extracting text from page in {file_path}: {str(e)}")
                    continue
        except Exception as e:
            print(f"Error reading PDF file {file_path}: {str(e)}")
            raise  # Re-raise the exception to handle it in the calling method

        return text

    def clean_text(self, text):
        try:
            # Remove extra spaces
            text = re.sub(r'\s+', ' ', text).strip()
            #text = re.sub(r"[^\u0600-\u06FF\s]", "", text)  # Supprimer tout sauf arabe et espaces

            # Supprime tous les diacritiques (tashkeel)
            #text = re.sub(r'[\u064B-\u065F\u0670]', '', text)

            # Normalisation des caractères arabes
            #text = re.sub(r'[أإآ]', 'ا', text)  # Normalise les différentes formes de alif
            #text = re.sub(r'ة', 'ه', text)  # Convertit le ta marbuta en ha
            #text = re.sub(r'ى', 'ي', text)  # Convertit l'alif maqsura en ya
            #text = re.sub(r'ؤ', 'ء', text)
            #text = re.sub(r'ئ', 'ء', text)
            # Supprime les caractères non-arabes
            #text = re.sub(r'[^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\s,;،:،؟!\.\[\]\(\)\{\}<>]','',text)

        except Exception as e:
            print(f"Error cleaning text: {str(e)}")
            return text  # Return original text if cleaning fails

        return text

    def read_stop_words(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                stop_words = set(f.read().splitlines())
                '''
                for line in f:
                    word = line.strip()
                    if word:  # Skip empty lines
                        # Normalize Arabic characters and remove diacritics
                        normalized = (
                            word
                            .replace('أ', 'ا')
                            .replace('إ', 'ا')
                            .replace('آ', 'ا')
                            .replace('ى', 'ي')
                            .replace('ة', 'ه')
                            .replace('ؤ', 'ء')
                            .replace('ئ', 'ء')
                            .strip()
                        )
                        stop_words.add(normalized)
                '''
                return stop_words

        except FileNotFoundError:
            print(f"Error: Stop words file not found at {file_path}")
            return set()
        except Exception as e:
            print(f"Error reading stop words file: {str(e)}")
            return set()
    def read_dictionary(self):
        # Load dictionary files with robust encoding handling
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
                # Try UTF-8 first, fall back to other encodings if needed
                for encoding in ['utf-8', 'windows-1256', 'iso-8859-6']:
                    try:
                        with open(dict_file, 'r', encoding=encoding) as f:
                            dictionary_words.update(line.strip() for line in f if line.strip())
                        break  # Successfully read file
                    except UnicodeDecodeError:
                        continue
                else:
                    print(f"Warning: Could not decode dictionary file - {dict_file}")
            except FileNotFoundError:
                print(f"Warning: Dictionary file not found - {dict_file}")
            except Exception as e:
                print(f"Error loading dictionary {dict_file}: {str(e)}")
        return dictionary_words


