import re


class ArabicTokenizer:
    def __init__(self):
        # Regex to remove Arabic numerals (٠١٢٣٤٥٦٧٨٩)
        self.arabic_numerals = re.compile(r'[\u0660-\u0669\u06F0-\u06F9]')

        # Regex to remove Arabic punctuation: ، ؛ ؟ « »
        self.arabic_punctuation = re.compile(r'[\u060C\u061B\u061F\u00AB\u00BB]')

        # Regex to remove Tashkeel (Arabic diacritics/vowel marks)
        self.tashkeel = re.compile(r'[\u064B-\u065F\u0610-\u061A\u0670]')

        # Regex for pure Arabic words (2+ letters)
        self.arabic_only = re.compile(
            r'^[^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]*'  # Remove leading non-Arabic
            r'([\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]{2,})'  # Keep Arabic core
            r'[^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]*$'  # Remove trailing non-Arabic
        )

    def clean_token(self, token):
        """Remove numerals, punctuation, tashkeel, and extract pure Arabic words"""
        # Step 1: Remove Arabic numerals
        token = self.arabic_numerals.sub('', token)
        # Step 2: Remove Arabic punctuation
        token = self.arabic_punctuation.sub('', token)
        # Step 3: Remove Tashkeel (diacritics)
        token = self.tashkeel.sub('', token)
        # Step 4: Extract pure Arabic words (2+ letters)
        match = self.arabic_only.search(token)
        return match.group(1) if match else ""

    def normalize_arabic(self, text):
        """Normalize Arabic text and handle concatenated words"""
        # Normalize characters first
        text = re.sub(r'[ًٌٍَُِّْـ]', '', text)  # Remove diacritics
        text = re.sub(r'[إأآا]', 'ا', text)  # Normalize Alif
        text = re.sub(r'ى', 'ي', text)  # Normalize Alef Maqsura
        text = re.sub(r'ؤ', 'و', text)  # Normalize Waw with Hamza
        text = re.sub(r'ئ', 'ي', text)  # Normalize Yeh with Hamza
        text = re.sub(r'ة', 'ه', text)  # Normalize Teh Marbuta
        return text

    def tokenize(self, text):
        """Get clean Arabic tokens (no numbers, punctuation, or tashkeel)"""
        return [
            self.clean_token(word) for word in text.split()
            if self.clean_token(word)
        ]