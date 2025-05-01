import os
import time
import logging
from PyQt5.QtWidgets import QApplication
import sys
import json
from .reader import PDFReader
from .processor import TextProcessor
from .tokenizer import ArabicTokenizer
from .analyzer import FrequencyAnalyzer
from .VocabularyChecker import VocabularyChecker
from .interface import ArabicPredictorGUI
from .utils import JSONUtils
from .matrix_builder import WordLevelMatrixBuilder, CharLevelMatrixBuilder
from .matrix_visualizer import MatrixVisualizer


class ArabicNLPPipeline:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing ArabicNLPPipeline components...")

        # Initialize components
        self.reader = PDFReader()
        self.processor = TextProcessor()
        self.tokenizer = ArabicTokenizer()
        self.analyzer = FrequencyAnalyzer()
        self.utils = JSONUtils()
        #self.vocab_cheker = VocabularyChecker()

        self.word_matrix_builder = WordLevelMatrixBuilder(config)
        self.char_matrix_builder = CharLevelMatrixBuilder(config)
        self.visualizer = MatrixVisualizer(config)

        # Initialize data variables
        self._initialize_data_vars()

        self.logger.info("Pipeline initialized successfully with all components")

    def _initialize_data_vars(self):
        """Initialize all data variables"""
        self.logger.debug("Initializing data variables")
        self.corpus = None
        self.stop_words = None
        self.all_tokens = None
        self.word_frequence_0 = None
        self.filtered_vocab = None
        self.not_stop_word = None
        self.dictionary_size = None
        self.rejected_vocab = None
        self.phrases = None

        # Statistics counters
        self.num_stopword = 0
        self.num_dictionary = 0
        self.num_stemmed = 0
        self.num_lemmed = 0
        self.num_ner = 0

    def run(self):
        """Main execution with GUI option"""
        self.logger.info("Starting main pipeline execution")
        print("1. Run full pipeline")
        print("2. Run GUI predictor")
        choice = input("Select option (1/2): ")

        if choice == "1":
            self.logger.info("User selected full pipeline execution")
            self.run_pipeline()
        elif choice == "2":
            self.logger.info("User selected GUI predictor")
            self.run_gui()
        else:
            self.logger.warning(f"Invalid option selected: {choice}")
            print("Invalid option")

    def run_pipeline(self):
        """Run the complete NLP pipeline"""
        self.logger.info("Starting full pipeline execution")
        try:
            self.load_stop_words()
            self.load_or_create_corpus()
            # self.tokenize_text()
            # self.analyze_vocabulary()
            # self.load_dictionary()
            # self.vocabulary_final()
            # self.display_statistics()
            self.process_phrases()
            self.build_matrices()
            self.generate_visualizations()
            self.logger.info("Pipeline completed successfully")
        except Exception as e:
            self.logger.error(f"Pipeline execution failed: {str(e)}", exc_info=True)
            raise

    def load_stop_words(self):
        """Load stop words from file"""
        self.logger.info(f"Loading stop words from {self.config['stop_words_file']}")
        try:
            self.stop_words = self.reader.read_stop_words(self.config["stop_words_file"])
            self.logger.info(f"Successfully loaded {len(self.stop_words)} stop words")
        except Exception as e:
            self.logger.error(f"Failed to load stop words: {str(e)}", exc_info=True)
            raise

    def load_or_create_corpus(self):
        """Load corpus from file or create from PDFs"""
        if not os.path.exists(self.config["corpus_file"]):
            self.logger.info(f"Corpus file not found, creating from PDFs in {self.config['pdf_directory']}")
            try:
                self.corpus = self.reader.read_pdfs_from_directory(
                    self.config["pdf_directory"],
                    self.config["corpus_file"]
                )
                self.logger.info(f"Successfully created corpus with {len(self.corpus)} characters")
            except Exception as e:
                self.logger.error(f"Failed to create corpus from PDFs: {str(e)}", exc_info=True)
                raise
        else:
            self.logger.info(f"Loading existing corpus from {self.config['corpus_file']}")
            try:
                with open(self.config["corpus_file"], "r", encoding="utf-8") as file:
                    self.corpus = file.read()
                self.logger.info(f"Successfully loaded corpus with {len(self.corpus)} characters")
            except Exception as e:
                self.logger.error(f"Failed to load corpus: {str(e)}", exc_info=True)
                raise

    def tokenize_text(self):
        """Tokenize corpus and filter stop words"""
        self.logger.info("Starting text tokenization")
        try:
            self.all_tokens = self.tokenizer.tokenize(self.corpus)
            self.logger.info(f"Tokenization completed. Total tokens: {len(self.all_tokens)}")
        except Exception as e:
            self.logger.error(f"Tokenization failed: {str(e)}", exc_info=True)
            raise

    def analyze_vocabulary(self):
        """Analyze and save vocabulary data"""
        self.logger.info("Starting vocabulary analysis")
        try:
            # Save vocabularies
            self.utils.save_in_json(self.all_tokens, self.config["vocab_0_all_tokens"])
            self.logger.debug(f"Saved all tokens to {self.config['vocab_0_all_tokens']}")

            # Calculate frequencies
            word_freq_0 = self.analyzer.calculate_word_frequencies(self.all_tokens)
            self.word_frequence_0 = self.analyzer.prepare_word_frequency_data(word_freq_0, len(self.all_tokens))

            self.utils.save_in_json(self.word_frequence_0, self.config["Vocabulary0"])
            self.logger.info(f"Vocabulary analysis completed. Saved frequency data to {self.config['Vocabulary0']}")
        except Exception as e:
            self.logger.error(f"Vocabulary analysis failed: {str(e)}", exc_info=True)
            raise

    def load_dictionary(self):
        """Load stop words from file"""
        self.logger.info("Loading dictionary")
        try:
            self.dictionary_size = self.reader.read_dictionary()
            self.logger.info(f"Dictionary loaded with {len(self.dictionary_size)} entries")
        except Exception as e:
            self.logger.error(f"Failed to load dictionary: {str(e)}", exc_info=True)
            raise

    def vocabulary_final(self):
        """Create final vocabulary through multi-stage filtering"""
        self.logger.info("Starting final vocabulary processing")
        if self.word_frequence_0 is None:
            error_msg = "Word frequency data not initialized"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        final_vocab = []
        rejected_words = []
        PROCESSING_BATCH = 5000
        COOLING_TIME = 5

        self.logger.info(f"Processing {len(self.word_frequence_0)} words in batches of {PROCESSING_BATCH}")

        for i, word_data in enumerate(self.word_frequence_0):
            word = word_data['Word']

            # Cooling system
            if i > 0 and i % PROCESSING_BATCH == 0:
                self.logger.debug(
                    f"Processed {i}/{len(self.word_frequence_0)} words. Cooling for {COOLING_TIME} seconds...")
                time.sleep(COOLING_TIME)

            is_in_stopwords = self.vocab_cheker.is_stop_word(word, self.stop_words)

            if is_in_stopwords:
                self.num_stopword += 1
            else:
                is_in_dict = self.vocab_cheker.is_in_dictionary(word, self.dictionary_size)

                if is_in_dict:
                    word_data['Identification'] = "Dictionary"
                    self.num_dictionary += 1
                    final_vocab.append(word_data)
                else:
                    is_in_stemmed = self.vocab_cheker.has_stemming(word)
                    if is_in_stemmed:
                        word_data['Identification'] = "Stemming"
                        self.num_stemmed += 1
                        final_vocab.append(word_data)
                    else:
                        is_in_lemmed = self.vocab_cheker.has_lemmatization(word)
                        if is_in_lemmed:
                            word_data['Identification'] = "Lemmatization"
                            self.num_lemmed += 1
                            final_vocab.append(word_data)
                        else:
                            is_in_ner = self.vocab_cheker.is_named_entity(word)
                            if is_in_ner:
                                word_data['Identification'] = "NER"
                                self.num_ner += 1
                                final_vocab.append(word_data)
                            else:
                                self.logger.debug(f"Rejected word: {word}")
                                rejected_words.append(word_data)

        # Save results
        self.utils.save_in_json(final_vocab, self.config["Vocab_Final"])
        self.utils.save_in_json(rejected_words, self.config["rejected_words_file"])
        self.filtered_vocab = final_vocab
        self.rejected_vocab = rejected_words

        self.logger.info(
            f"Final vocabulary processing completed. Accepted: {len(final_vocab)}, Rejected: {len(rejected_words)}")

    def display_statistics(self):
        """Display pipeline statistics"""
        self.logger.info("Displaying pipeline statistics")
        stats = {
            "Total Stop Words": len(self.stop_words),
            "Total Tokens (Vocabulary 0)": len(self.all_tokens),
            "Unique Words (Vocabulary 0)": len(set(self.all_tokens)),
            "Total Dictionary Words": len(self.dictionary_size),
            "Words in Stop Words": self.num_stopword,
            "Words in Dictionary": self.num_dictionary,
            "Words in Stemming": self.num_stemmed,
            "Words in Lemmatization": self.num_lemmed,
            "Words in NER": self.num_ner,
            "Final vocabulary size": len(self.filtered_vocab),
            "Rejected words": len(self.rejected_vocab)
        }

        for stat, value in stats.items():
            print(f"{stat}: {value}")
            self.logger.info(f"{stat}: {value}")

        self.logger.info("Statistics displayed successfully")

    def process_phrases(self):
        """Process text into phrases"""
        self.logger.info("Starting phrase processing")
        try:
            self.phrases = self.processor.split_into_phrases(self.corpus)
            self.utils.save_in_json(self.phrases, self.config["phrases_file"])
            self.logger.info(f"Processed {len(self.phrases)} phrases and saved to {self.config['phrases_file']}")
            print(f"Total Phrases is : {len(self.phrases)} phrase")
        except Exception as e:
            self.logger.error(f"Phrase processing failed: {str(e)}", exc_info=True)
            raise

    def build_matrices(self):
        """Build word and character level matrices"""
        self.logger.info("Starting matrix building process")

        try:
            self.logger.info("Building word-level matrix")
            self.word_matrix_builder.load_vocabulary()
            self.word_matrix_builder.load_phrases()
            self.word_matrix_builder.build_from_phrases()
            self.word_matrix_builder.save_matrix()
            self.logger.info("Word-level matrix built successfully")

            self.logger.info("Building character-level matrix")
            self.char_matrix_builder.load_vocabulary()
            self.char_matrix_builder.build_from_vocabulary()
            self.char_matrix_builder.save_matrix()
            self.logger.info("Character-level matrix built successfully")

        except Exception as e:
            self.logger.error(f"Matrix building failed: {str(e)}", exc_info=True)
            raise

    def run_gui(self):


        """Run the Arabic word prediction GUI"""
        self.logger.info("Starting GUI application")

        if not os.path.exists(self.config["word_matrix_file"]):
            self.logger.warning("Word matrix not found, building matrices first")
            self.build_matrices()

        try:
            app = QApplication(sys.argv)
            font = app.font()
            font.setFamily("Arial")
            font.setPointSize(12)
            app.setFont(font)

            window = ArabicPredictorGUI(self.config)
            window.show()

            self.logger.info("GUI started successfully")
            sys.exit(app.exec_())
        except Exception as e:
            self.logger.error(f"GUI failed to start: {str(e)}", exc_info=True)
            raise

    def generate_visualizations(self):
        """Generate matrix visualizations"""
        self.logger.info("Starting visualization generation")
        try:
            visualizer = MatrixVisualizer(self.config)
            #visualizer.plot_word_graph()
            visualizer.plot_char_graph()
            visualizer.plot_char_heatmap()
            self.logger.info("Visualizations generated successfully")
        except Exception as e:
            error_msg = f"Visualization generation failed: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            print(f"❌ {error_msg}")