import os
from .reader import PDFReader
from .processor import TextProcessor
from .tokenizer import ArabicTokenizer
from .analyzer import FrequencyAnalyzer
from .utils import JSONUtils


class ArabicNLPPipeline:
    def __init__(self, config):
        self.config = config
        self.reader = PDFReader()
        self.processor = TextProcessor()
        self.tokenizer = ArabicTokenizer()
        self.analyzer = FrequencyAnalyzer()
        self.utils = JSONUtils()

        # Initialize data holders
        self.corpus = None
        self.stop_words = None
        self.all_tokens = None
        self.filtered_tokens = None

    def run(self):
        """Execute the complete NLP pipeline"""
        self.load_stop_words()
        self.load_or_create_corpus()
        self.tokenize_text()
        self.analyze_vocabulary()
        self.display_statistics()
        self.process_phrases()

    def load_stop_words(self):
        """Load stop words from file"""
        self.stop_words = self.reader.read_stop_words(self.config["stop_words_file"])

    def load_or_create_corpus(self):
        """Load corpus from file or create from PDFs"""
        if not os.path.exists(self.config["corpus_file"]):
            self.corpus = self.reader.read_pdfs_from_directory(
                self.config["pdf_directory"],
                self.config["corpus_file"]
            )
        else:
            with open(self.config["corpus_file"], "r", encoding="utf-8") as file:
                self.corpus = file.read()

    def tokenize_text(self):
        """Tokenize corpus and filter stop words"""
        self.all_tokens = self.tokenizer.tokenize(self.corpus)
        self.filtered_tokens = [word for word in self.all_tokens if word not in self.stop_words]

    def analyze_vocabulary(self):
        """Analyze and save vocabulary data"""
        # Save vocabularies
        self.utils.save_in_json(self.all_tokens, self.config["vocab_0_file"])
        self.utils.save_in_json(self.filtered_tokens, self.config["vocab_1_file"])

        # Calculate frequencies
        word_freq_0 = self.analyzer.calculate_word_frequencies(self.all_tokens)
        word_freq_1 = self.analyzer.calculate_word_frequencies(self.filtered_tokens)

        # Prepare and save frequency data
        word_frequence_0 = self.analyzer.prepare_word_frequency_data(word_freq_0, len(self.all_tokens))
        word_frequence_1 = self.analyzer.prepare_word_frequency_data(word_freq_1, len(self.filtered_tokens))

        self.utils.save_in_json(word_frequence_0, self.config["word_freq_0_file"])
        self.utils.save_in_json(word_frequence_1, self.config["word_freq_1_file"])

    def display_statistics(self):
        """Display pipeline statistics"""
        print("Total Tokens (Vocabulary 0):", len(self.all_tokens))
        print("Unique Words (Vocabulary 0):", len(set(self.all_tokens)))
        print("Total Tokens (Vocabulary 1):", len(self.filtered_tokens))
        print("Unique Words (Vocabulary 1):", len(set(self.filtered_tokens)))
        print("Pipeline completed!")


    def process_phrases(self):
        """Process corpus into phrases and return them"""
        phrases = self.processor.process_text_file(self.corpus, self.config["phrases_file"])
        print("phrases:", len(phrases))