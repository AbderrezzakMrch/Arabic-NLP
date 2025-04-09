import re
from pyarabic.araby import strip_tashkeel, normalize_hamza
from pyarabic.araby import is_arabicword


class ArabicTokenizer:
    def __init__(self):
        """Initialize with PyArabic's normalizers"""
        pass

    def _normalize_arabic(self, text):
        """Comprehensive Arabic text normalization"""
        # Step 1: Remove diacritics
        text = strip_tashkeel(text)

        # Step 2: Normalize hamza
        text = normalize_hamza(text)

        # Step 3: Remove non-Arabic characters (manual implementation)
        arabic_chars = r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+'  # All Arabic Unicode blocks
        text = ' '.join(re.findall(arabic_chars, text))

        return text.strip()

    def is_arabic(self, word):
        """Check if word is Arabic using PyArabic's validator"""
        return is_arabicword(word)

    def tokenize(self, text):
        """Arabic tokenization with normalization"""
        text = self._normalize_arabic(text)
        words = re.findall(r'[ء-ي]{2,}', text)  # 2+ Arabic letters
        return [word for word in words if self.is_arabic(word)]