import os
from modules.reader import read_pdfs_from_directory, read_stop_words
from modules.processor import process_text_file
from modules.tokenizer import tokenize
from modules.analyzer import calculate_word_frequencies, prepare_word_frequency_data
from modules.utils import save_in_json

def main():
    # Paths to all files
    stop_words_file = "data/stop_arabic.txt"
    pdf_directory = "data/pdf_files/"
    corpus_file = "data/corpus.txt"
    phrases_file = "data/phrases.json"
    vocab_0_file = "data/vocabulary_0.json"
    vocab_1_file = "data/vocabulary_1.json"
    word_freq_0_file = "data/word_freq_0.json"
    word_freq_1_file = "data/word_freq_1.json"

    # Read stop words
    stop_words = read_stop_words(stop_words_file)

    # Read and clean text from all PDFs
    if not os.path.exists(corpus_file):
        corpus = read_pdfs_from_directory(pdf_directory, corpus_file)
    else:
        with open(corpus_file, "r", encoding="utf-8") as file:
            corpus = file.read()

    # Step 1: Process text into phrases
    phrases = process_text_file(corpus, phrases_file)

    # Step 2: Tokenize each phrase
    all_tokens = []
    for phrase in phrases:
        tokens = tokenize(phrase)
        all_tokens.extend(tokens)

    # Save Vocabulary 0 (All Arabic tokens)
    save_in_json(all_tokens, vocab_0_file)

    # Step 3: Remove stop words
    filtered_tokens = [word for word in all_tokens if word not in stop_words]

    # Save Vocabulary 1 (Arabic tokens without stop words)
    save_in_json(filtered_tokens, vocab_1_file)

    # Step 4: Calculate word frequencies for both vocabularies
    word_freq_0 = calculate_word_frequencies(all_tokens)
    word_freq_1 = calculate_word_frequencies(filtered_tokens)

    # Step 5: Prepare word frequency data for JSON
    word_frequence_0 = prepare_word_frequency_data(word_freq_0, len(all_tokens))
    word_frequence_1 = prepare_word_frequency_data(word_freq_1, len(filtered_tokens))

    # Step 6: Save word frequencies separately
    save_in_json(word_frequence_0, word_freq_0_file)
    save_in_json(word_frequence_1, word_freq_1_file)

    # Print statistics
    print("Total Tokens (Vocabulary 0):", len(all_tokens))
    print("Unique Words (Vocabulary 0):", len(set(all_tokens)))
    print("Total Tokens (Vocabulary 1):", len(filtered_tokens))
    print("Unique Words (Vocabulary 1):", len(set(filtered_tokens)))
    print("Pipeline completed!")

if __name__ == "__main__":
    main()
