import re


class ArabicTokenizer:
    def is_arabic(self, word):
        return bool(re.fullmatch(r'[\u0600-\u06FF]+', word))

    def tokenize(self, text):
        # Match Arabic words of at least 2 letters
        words = re.findall(r'\b[ء-ي]{2,}\b', text)

        # Filter out non-Arabic words
        words = [word for word in words if self.is_arabic(word)]

        return words