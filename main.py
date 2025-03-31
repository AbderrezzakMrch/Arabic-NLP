# main.py
import os
import json
from modules.reader import read_pdfs_from_directory, read_pdf
from modules.phrase_splitter import split_into_phrases
from modules.next_word_matrix import create_next_word_matrix
from modules.char_transition_matrix import create_global_char_transition_matrix
from modules.tokenizer import tokenize
from modules.stemmer import stem_words
from modules.analyzer import calculate_word_frequencies, prepare_word_frequency_data
from modules.utils import save_in_json

def main():
    # Paths
    stop_words_file = "data/stop_arabic.txt"
    pdf_directory = "data/pdf_files"
    corpus_file = "data/corpus.txt"
    phrases_file = "data/phrases.json"
    next_word_matrix_file = "data/next_word_matrix.json"
    char_transition_matrix_file = "data/char_transition_matrix.json"
    tokens_file = "data/tokens.json"
    word_freq_file = "data/word_freq.json"
    stemmed_file = "data/stemmed.json"

    # Step 1: Read stop words
    with open(stop_words_file, "r", encoding="utf-8") as file:
        stop_words = set(file.read().splitlines())

    # Step 2: Read PDFs and save combined text (only if not already done)
    if not os.path.exists(corpus_file):
        read_pdfs_from_directory(pdf_directory, corpus_file)

    # Step 3: Split text into phrases
    with open(corpus_file, "r", encoding="utf-8") as file:
        corpus = file.read()
    phrases = split_into_phrases(corpus)
    save_in_json(phrases, phrases_file)

    # Step 4: Create next-word matrices
    next_word_matrices = create_next_word_matrix(phrases)
    save_in_json(next_word_matrices, next_word_matrix_file)

    # Step 5: Create global character transition matrix
    char_transition_matrix = create_global_char_transition_matrix(corpus)
    save_in_json(char_transition_matrix, char_transition_matrix_file)

    # Step 6: Tokenize the text (only if not already done)
    if not os.path.exists(tokens_file):
        indexed_tokens = tokenize(corpus)  # Use qalsadi tokenizer
        tokens = list(indexed_tokens.values())  # Extract words without indices
        save_in_json(indexed_tokens, tokens_file)
    else:
        with open(tokens_file, "r", encoding="utf-8") as file:
            indexed_tokens = json.load(file)
        tokens = list(indexed_tokens.values())  # Extract words without indices

    # Step 7: Calculate word frequencies
    word_freq = calculate_word_frequencies(tokens, stop_words)
    word_frequence = prepare_word_frequency_data(word_freq, len(tokens))
    save_in_json(word_frequence, word_freq_file)

    # Step 8: Stem the tokens (only if not already done)
    if not os.path.exists(stemmed_file):
        stemmed_words = stem_words(tokens)
        save_in_json(stemmed_words, stemmed_file)

    # Print statistics
    print("Total Phrases:", len(phrases))
    print("Total Words:", len(tokens))
    print("Unique Words:", len(word_freq))

    print("Pipeline completed!")

if __name__ == "__main__":
    main()