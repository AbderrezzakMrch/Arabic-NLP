# modules/phrase_splitter.py
import re


def clean_text(text):
    """
    Clean the text by removing numbers, special characters, and newlines.

    :param text: Input Arabic text as a string.
    :return: Cleaned text as a string.
    """
    # Remove numbers
    text = re.sub(r'\d+', '', text)

    # Remove special characters (e.g., -, /, etc.)
    text = re.sub(r'[^\w\s\u0600-\u06FF]', ' ', text)

    # Remove newlines and replace with spaces
    text = text.replace('\n', ' ')

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def split_into_phrases(text):
    """
    Split text into phrases using punctuation marks after cleaning the text.

    :param text: Input Arabic text as a string.
    :return: List of phrases.
    """
    # Clean the text
    cleaned_text = clean_text(text)

    # Split by common Arabic punctuation marks
    phrases = re.split(r'[.؟!،][\u0600-\u06FF\u061B\u061F\u0640\u0660-\u0669\u066A\u066B\u066C\u066D\u067E\u0686\u06AF\u06A4\u06A9\u06CC\u06F0-\u06F9]+', cleaned_text)

    # Remove empty phrases and strip whitespace
    phrases = [phrase.strip() for phrase in phrases if phrase.strip()]

    return phrases