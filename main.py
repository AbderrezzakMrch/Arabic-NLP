from modules.pipeline import ArabicNLPPipeline

def main():
    # Configuration
    config = {
        "stop_words_file": "data/stop_arabic.txt",
        "pdf_directory": "data/pdf_files/",
        "corpus_file": "data/corpus.txt",
        "vocab_0_file": "data/vocabulary_0.json",
        "vocab_1_file": "data/vocabulary_1.json",
        "word_freq_0_file": "data/word_freq_0.json",
        "word_freq_1_file": "data/word_freq_1.json",
        "phrases_file": "data/phrases.json"
    }

    # Create and run pipeline
    pipeline = ArabicNLPPipeline(config)
    pipeline.run()

if __name__ == "__main__":
    main()