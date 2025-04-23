from farasa.stemmer import FarasaStemmer
import json


class ArabicStemmer:
    def __init__(self):
        """Initialize Farasa stemmer"""
        self.stemmer = FarasaStemmer()

    def stem_text(self, text):
        """Stem a single text string"""
        return self.stemmer.stem(text)

    def stem_phrases(self, phrases, output_file):


        stemmed = [self.stem_text(phrase) for phrase in phrases]

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(stemmed, f, ensure_ascii=False, indent=4)

        print(f"Stemmed phrases saved to {output_file}")
        return stemmed