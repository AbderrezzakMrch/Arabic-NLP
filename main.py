import logging
from modules.pipeline import ArabicNLPPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    # dictionary contains all path batch nsauvragrdo
    config = {
        "stop_words_file": "data/stop_arabic.txt",
        "pdf_directory": "data/pdf_files/",
        "corpus_file": "data/corpus.txt",
        "vocab_0_all_tokens": "data/vocabulary_0.json",
        "vocab_1_file": "data/vocabulary_1.json",
        "Vocabulary0": "data/word_freq_0.json",
        "word_freq_1_file": "data/word_freq_1.json",
        "Vocab_Final": "data/Vocab_Final.json",
        "dictionary_file": "data/a1rabic_dictionary.txt",
        "rejected_words_file": "data/rejected_words.json",
        "phrases_file": "data/phrases.json",
        "stemmed_phrases_file": "data/stemmed_phrases.json",
        "lemmatized_phrases_file": "data/lemmatized_phrases.json",
        "ner_phrases_file": "data/ner_phrases.json",
        "word_pred_file": "data/word_predictor.json",
        "char_pred_file": "data/char_predictor.json",
        "word_matrix_file": "data/next_word.json",
        "char_matrix_file": "data/next_char.json",
        "output_dir": "outputs"
    }

    logger.info("Starting Arabic NLP Pipeline")
    logger.debug(f"Configuration: {config}")

    # Create and run pipeline
    pipeline = ArabicNLPPipeline(config)
    try:
        logger.info("Pipeline execution started")
        pipeline.run()
        logger.info("Pipeline executed successfully")
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
        print(f"❌ Pipeline failed: {str(e)}")

if __name__ == "__main__":
    logger.info("Application started")
    main()
    logger.info("Application finished")