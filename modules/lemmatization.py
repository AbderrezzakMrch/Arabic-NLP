from farasa.segmenter import FarasaSegmenter
import re
import json


class ArabicLemmer:
    def __init__(self, keep_segmentation=False):
        """
        Args:
            keep_segmentation: If False, removes Farasa's + markers and cleans prefixes/suffixes
        """
        self.segmenter = FarasaSegmenter()
        self.keep_segmentation = keep_segmentation

    def lem_text(self, text):
        segmented = self.segmenter.segment(text)

        if not self.keep_segmentation:
            # Step 1: Remove segmentation markers
            clean_text = re.sub(r'\+(?!$)', '', segmented)  # Keep final + for feminine ة

            # Step 2: Remove common prefixes/suffixes
            clean_text = self._remove_affixes(clean_text)
            return clean_text
        return segmented

    def _remove_affixes(self, text):
        """Advanced Arabic affix removal"""
        # Common prefixes (al-, wa-, fa-, etc.)
        text = re.sub(r'^(ال|وال|فال|بال|ولل|لل|ب|ف|و|ل|ك|س|ي)', '', text)

        # Common suffixes (-hum, -ka, -ha, etc.)
        text = re.sub(r'(ها|هم|هما|هن|نا|كم|كما|كن|ي|ك|ه|ة)$', '', text)

        return text.strip()

    def lem_phrases(self, phrases, output_file=None):
        lemmed = []
        for phrase in phrases:
            if isinstance(phrase, list):  # Handle tokenized input
                lemmed.append([self.lem_text(word) for word in phrase])
            else:
                lemmed.append(self.lem_text(phrase))

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(lemmed, f, ensure_ascii=False, indent=4)
            print(f"Lemmatized phrases saved to {output_file}")
        return lemmed