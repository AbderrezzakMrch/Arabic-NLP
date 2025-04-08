import re
from .utils import JSONUtils

class TextProcessor:
    def __init__(self):
        self.utils = JSONUtils()

    def split_into_phrases(self, text):
        """
        Splits Arabic text into meaningful phrases:
        - Sentences end at `.`, `؟`, `!`, `،`
        - Extracts nested phrases inside `[...]` and `(...)`
        """
        sentences = re.split(r'(?<=[.؟!،])\s*', text)  # Arabic punctuation handling
        phrases = []

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Extract nested phrases inside `[...]` and `(...)`
            matches = re.findall(r'\[([^]]+)\]|\(([^)]+)\)', sentence)

            # Remove brackets/parentheses from the main sentence
            clean_sentence = re.sub(r'\[.*?\]|\(.*?\)', '', sentence).strip()

            # Add main sentence if it's not empty
            if clean_sentence:
                phrases.append(clean_sentence)

            # Add extracted nested phrases separately
            for match in matches:
                for phrase in match:
                    if phrase:
                        phrases.append(phrase.strip())

        return phrases

    def clean_phrases(self, phrases):
        """
        Cleans Arabic phrases by:
        - Removing numbers
        - Removing special characters like `؟!.,;:§_-/"'|()`
        - Removing extra spaces
        """
        cleaned_phrases = []
        for phrase in phrases:
            phrase = re.sub(r'\d+', '', phrase)  # Remove numbers
            phrase = re.sub(r'[؟!.,،;:§_\-/|\"\'()]', '', phrase)  # Remove special characters
            phrase = re.sub(r'\s+', ' ', phrase).strip()  # Remove extra spaces
            if phrase:
                cleaned_phrases.append(phrase)

        return cleaned_phrases

    def process_text_file(self, text, output_json):
        """
        Splits Arabic text into phrases, cleans them, and saves to a JSON file.
        """
        phrases = self.split_into_phrases(text)  # Step 1: Split into phrases
        cleaned_phrases = self.clean_phrases(phrases)  # Step 2: Clean each phrase

        self.utils.save_in_json(cleaned_phrases, output_json)
        print(f"Phrases saved to {output_json}")
        return cleaned_phrases