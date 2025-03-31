import re

def is_arabic(word):
    """
    Check if a word is entirely in Arabic.
    
    :param word: Input word.
    :return: True if it's Arabic, False otherwise.
    """
    return bool(re.fullmatch(r'[\u0600-\u06FF]+', word))

def tokenize(text):
    """
    Tokenize Arabic text and remove invalid words.
    
    :param text: Input Arabic text.
    :return: List of Arabic words.
    """
    # Match Arabic words of at least 2 letters
    words = re.findall(r'\b[ء-ي]{2,}\b', text)
    
    # Filter out non-Arabic words
    words = [word for word in words if is_arabic(word)]
    
    return words