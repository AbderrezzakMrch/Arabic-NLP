import re


class ArabicTokenizer:
    def __init__(self):
        # Arabic Unicode ranges + basic punctuation
        self.arabic_pattern = re.compile(
            r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+'
        )

    def is_arabic(self, word):
        """Check if word is valid Arabic (2+ letters)"""
        return (len(word) >= 2 and
                bool(re.fullmatch(r'^[\u0600-\u06FF]+$', word)))

    def clean_token(self, token):
        """Remove ALL non-Arabic characters from a token"""
        # Find all Arabic letter sequences in the token
        arabic_parts = self.arabic_pattern.findall(token)
        # Return the longest Arabic part (if any)
        return max(arabic_parts, key=len) if arabic_parts else ""

    def tokenize(self, text):
        """Manual tokenization by splitting on whitespace"""
        # 1. Split on any whitespace
        raw_tokens = re.split(r'\s+', text.strip())

        # 2. Clean each token
        tokens = []
        for token in raw_tokens:
            cleaned = self.clean_token(token)
            if self.is_arabic(cleaned):
                tokens.append(cleaned)

        return tokens