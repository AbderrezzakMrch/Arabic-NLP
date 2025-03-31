# modules/tokenizer.py
import re
from qalsadi.analex import Analex


def is_arabic(word):
    """
    Check if a word is Arabic by verifying if all its characters are within the Arabic Unicode range.

    :param word: Input word as a string.
    :return: True if the word is Arabic, False otherwise.
    """
    arabic_pattern = re.compile(
        r'[\u0600-\u06FF\u061B\u061F\u0640\u0660-\u0669\u066A\u066B\u066C\u066D\u067E\u0686\u06AF\u06A4\u06A9\u06CC\u06F0-\u06F9]+')
    return bool(arabic_pattern.fullmatch(word))


def tokenize(text):
    """
    Tokenize Arabic text using qalsadi and filter out non-Arabic words, numbers, and punctuation.

    :param text: Input Arabic text as a string.
    :return: Dictionary of tokenized Arabic words with index numbers.
    """
    # Initialize the qalsadi tokenizer
    tokenizer = Analex()

    # Tokenize the text using qalsadi
    tokens = tokenizer.tokenize(text)

    # Filter out non-Arabic words, numbers, and punctuation
    filtered_tokens = [word for word in tokens if is_arabic(word)]

    # Assign index numbers to tokens and convert to a dictionary
    indexed_tokens = dict(enumerate(filtered_tokens, start=1))

    return indexed_tokens