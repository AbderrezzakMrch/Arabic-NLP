# modules/next_word_matrix.py
from collections import defaultdict


def create_next_word_matrix(phrases):
    """
    Create a next-word matrix for each phrase.

    :param phrases: List of phrases.
    :return: Dictionary of next-word matrices.
    """
    next_word_matrices = {}

    for phrase in phrases:
        words = phrase.split()
        matrix = defaultdict(lambda: defaultdict(int))

        for i in range(len(words) - 1):
            current_word = words[i]
            next_word = words[i + 1]
            matrix[current_word][next_word] += 1

        next_word_matrices[phrase] = matrix

    return next_word_matrices