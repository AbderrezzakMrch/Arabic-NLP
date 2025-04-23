# import class pipline
from modules.pipeline import ArabicNLPPipeline

def main():
    # dictoinare conatins all path bach nsauvragrdo
    config = {
        "stop_words_file": "data/stop_arabic.txt",
        "pdf_directory": "data/pdf_files/",
        "corpus_file": "data/corpus.txt",
        "vocab_0_all_tokens": "data/vocabulary_0.json",
        "vocab_1_file": "data/vocabulary_1.json",
        "Vocabulary0": "data/word_freq_0.json",
        "word_freq_1_file": "data/word_freq_1.json",
        "Vocab_Final": "data/Vocab_Final.json",
        "dictionary_file": "data/arabic_dictionary.txt",
        "rejected_words_file": "data/rejected_words.json",
        "phrases_file": "data/phrases.json",
        "stemmed_phrases_file": "data/stemmed_phrases.json",
        "lemmatized_phrases_file": "data/lemmatized_phrases.json",
        "ner_phrases_file": "data/ner_phrases.json",
        "word_pred_file": "data/word_predictor.json",
        "char_pred_file": "data/char_predictor.json"
    }


    # Create and run pipeline
    pipeline = ArabicNLPPipeline(config)
    try:
        pipeline.run()
    except Exception as e:
        print(f"❌ Pipeline failed: {str(e)}")

if __name__ == "__main__":
    main()

    import logging
    from datetime import datetime
    import os


    def setup_logging():
        """Configure logging system"""
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"{log_dir}/arabic_nlp_{timestamp}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )


    def main():
        setup_logging()
        logger = logging.getLogger(__name__)

        config = {
            "stop_words_file": "data/stop_arabic.txt",
            "pdf_directory": "data/pdf_files/",
            "corpus_file": "data/corpus.txt",
            "vocab_0_all_tokens": "data/vocabulary_0.json",
            "Vocabulary0": "data/word_freq_0.json",
            "Vocab_Final": "data/Vocab_Final.json",
            "dictionary_file": "data/arabic_dictionary.txt",
            "rejected_words_file": "data/rejected_words.json",
            "output_dir": "output"
        }

        try:
            logger.info("Starting Arabic NLP Pipeline")
            pipeline = ArabicNLPPipeline(config)
            pipeline.run()
            logger.info("Pipeline completed successfully")
        except Exception as e:
            logger.error(f"Pipeline execution failed: {str(e)}")
            raise


    if __name__ == "__main__":
        main()