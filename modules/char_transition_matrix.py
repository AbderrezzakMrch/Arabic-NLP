# modules/char_transition_matrix.py
from collections import defaultdict


def create_global_char_transition_matrix(corpus):
    """
    Create a global character transition matrix for the entire corpus, excluding spaces, hyphens, and newlines.

    :param corpus: Input Arabic text as a string.
    :return: Dictionary representing the character transition matrix.
    """
    # Initialize the matrix
    matrix = defaultdict(lambda: defaultdict(int))

    # Iterate through the corpus
    for i in range(len(corpus) - 1):
        current_char = corpus[i]
        next_char = corpus[i + 1]

        # Skip spaces, hyphens, and newlines
        if current_char in [' ', '-', '\n'] or next_char in [' ', '-', '\n']:
            continue

        # Update the matrix
        matrix[current_char][next_char] += 1

    return matrix