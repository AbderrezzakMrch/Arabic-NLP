# modules/stemmer.py
from nltk.stem.isri import ISRIStemmer


def stem_word(word):
    """
    Stem an Arabic word.

    :param word: Input Arabic word as a string.
    :return: Stemmed word as a string.
    """
    stemmer = ISRIStemmer()
    return stemmer.stem(word)


def stem_words(words):
    """
    Stem a list of Arabic words.

    :param words: List of Arabic words.
    :return: List of stemmed words.
    """
    return [stem_word(word) for word in words]