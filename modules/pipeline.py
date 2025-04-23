import os
import time



#import from the class from file
from .reader import PDFReader
from .processor import TextProcessor
from .tokenizer import ArabicTokenizer
from .analyzer import FrequencyAnalyzer
from .VocabularyChecker import VocabularyChecker
from .stemmer import ArabicStemmer
from .utils import JSONUtils
from .lemmatization import ArabicLemmer
from .ner import ArabicNer
from .dict_updater import ArabicPredictor

class ArabicNLPPipeline:
    def __init__(self, config): # here im calling constructer of each class
        self.config = config
        self.reader = PDFReader()
        self.processor = TextProcessor()
        self.tokenizer = ArabicTokenizer()
        self.analyzer = FrequencyAnalyzer()
        self.vocab_cheker = VocabularyChecker()
        self.stemmer = ArabicStemmer()
        self.lemmer = ArabicLemmer()
        self.ner = ArabicNer()
        self.predictor = ArabicPredictor()
        self.utils = JSONUtils()



        # Initialize data variables bach n7t fihom les valeur
        self.corpus = None
        self.stop_words = None
        self.all_tokens = None
        #self.filtered_tokens = None
        self.word_frequence_0 = None
        self.filtered_vocab = None
        self.not_stop_word = None
        self.dictionary_size = None
        self.rejected_vocab = None
        self.phrases = None
        self.lemmatized_phrases = None
        self.nered_phrases = None


        self.num_stopword = 0
        self.num_dictionary = 0
        self.num_stemmed = 0
        self.num_lemmed = 0
        self.num_ner = 0

    def run(self):
        """Hna executina the main functions"""
        self.load_stop_words()
        self.load_or_create_corpus()
        self.tokenize_text()
        self.analyze_vocabulary()
        self.load_dictionary()
        self.vocabulary_final()
        self.display_statistics()
        #self.process_phrases()
        #self.stem_phrases()
        #self.lemmatize_phrases()
        #self.ner_phrases()
        #self.build_predictors()


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
        #self.filtered_tokens = [word for word in self.all_tokens if word not in self.stop_words]

    def analyze_vocabulary(self):
        """Analyze and save vocabulary data"""
        # Save vocabularies
        self.utils.save_in_json(self.all_tokens, self.config["vocab_0_all_tokens"])

        # Calculate frequencies
        word_freq_0 = self.analyzer.calculate_word_frequencies(self.all_tokens)

        # Prepare and save frequency data
        self.word_frequence_0 = self.analyzer.prepare_word_frequency_data(word_freq_0, len(self.all_tokens))

        self.utils.save_in_json(self.word_frequence_0, self.config["Vocabulary0"])

    def load_dictionary(self):
        """Load stop words from file"""
        self.dictionary_size = self.reader.read_dictionary()

    def vocabulary_final(self):
        """Create final vocabulary through multi-stage filtering with Farasa optimization"""
        if self.word_frequence_0 is None:
            raise ValueError("Word frequency data not initialized. Run analyze_vocabulary() first.")

        final_vocab = []
        rejected_words = []

        # Cooling system parameters
        PROCESSING_BATCH = 5000  # Number of words to process before cooling
        COOLING_TIME = 5       # Seconds to rest between batches
        start_time = time.time()


        for i, word_data in enumerate(self.word_frequence_0):
            print(f"process{ i} {len(set(self.all_tokens))}")
            word = word_data['Word']
            # Cooling system - take a break every PROCESSING_BATCH words
            if i > 0 and i % PROCESSING_BATCH == 0:
                print(f"\nProcessed {i}/{len(self.word_frequence_0)} words")
                print(f"Taking {COOLING_TIME} second cooling break...")
                time.sleep(COOLING_TIME)
                print("Resuming processing...\n")


            is_in_stopwords = self.vocab_cheker.is_stop_word(word,self.stop_words)
            # Stage 1: Stop word check
            if is_in_stopwords:
                word_data['Identification'] = "Stop Words"
                #print(f"Original: {word} | in stop words")
                self.num_stopword += 1
                final_vocab.append(word_data)

            else:
                is_in_dict = self.vocab_cheker.is_in_dictionary(word,self.dictionary_size)
                # Stage 2: Dictionary check
                if is_in_dict :
                    word_data['Identification'] = "Dictionary"
                    self.num_dictionary += 1
                    final_vocab.append(word_data)

                else:
                    #print(f"{word} not a Dictionary ===> Check Steamming")
                    # Stage 3: Farasa Stemming
                    is_in_stemmed = self.vocab_cheker.has_stemming(word)
                    if is_in_stemmed:
                        word_data['Identification'] = "Stemming"
                        self.num_stemmed += 1
                        # word_data['Stemmed'] = stemmed
                        final_vocab.append(word_data)
                    else:
                        #print(f"{word} has not Steamming ===> Check Lemmatization")
                        is_in_lemmed = self.vocab_cheker.has_lemmatization(word)
                        if is_in_lemmed:
                            word_data['Identification'] = "Lemmatization"
                            self.num_lemmed += 1
                            # word_data['Lemmatized'] = lemmatized
                            final_vocab.append(word_data)
                        else:
                            #print(f"{word} has not lemmatization ===> Check ner")
                            is_in_ner = self.vocab_cheker.is_named_entity(word)
                            if is_in_ner:  # Accept ANY tag except 'O'
                                word_data['Identification'] = "NER"
                                self.num_ner += 1
                                #word_data['NER'] = entity_tag
                                final_vocab.append(word_data)
                            else:
                                print(f"❌ Rejected: {word} (not an entity)")
                                rejected_words.append(word_data)
            # If all stages fail


        # Save results
        self.utils.save_in_json(final_vocab, self.config["Vocab_Final"])
        self.utils.save_in_json(rejected_words, self.config["rejected_words_file"])
        self.filtered_vocab = final_vocab  # For statistics
        self.rejected_vocab = rejected_words  # For statistics

    def display_statistics(self):
        """Display pipeline statistics"""
        print("Total Stop Words :", len(self.stop_words))
        print("Total Tokens (Vocabulary 0):", len(self.all_tokens))
        print("Unique Words (Vocabulary 0):", len(set(self.all_tokens)))
        print("Total Dictionary Words :", len(self.dictionary_size))
        #Vocaulary final statistiques
        print("Total Word in Stop Words : ",self.num_stopword)
        print("Total Word in Dictionary : ", self.num_dictionary)
        print("Total Word in Steamming : ", self.num_stemmed)
        print("Total Word in Lemmatization : ", self.num_lemmed)
        print("Total Word in NER : ", self.num_ner)

        print(f"Final vocabulary: {len(self.filtered_vocab)} words")
        print(f"Final Rejected Words: {len(self.rejected_vocab)} words")
        print("Pipeline completed!")


    def process_phrases(self):
        """Process corpus into phrases and return them"""
        self.phrases = self.processor.process_text_file(self.corpus, self.config["phrases_file"])
        print("phrases:", len(self.phrases))

    # Add new method for stemming
    def stem_phrases(self):
        """Process phrases through Farasa stemmer"""
        self.stemmer.stem_phrases(
            self.phrases,
            self.config["stemmed_phrases_file"]
        )
        print("complete steamming")

    def lemmatize_phrases(self):
        # For NER - keep segmentation
        self.lemmatized_phrases = self.lemmer.lem_phrases(
            self.phrases,
            self.config["lemmatized_phrases_file"]
        )
        print("complete lemmatization")

    def ner_phrases(self):
        self.nered_phrases = self.ner.ner_phrases(
            self.lemmatized_phrases,
            self.config["ner_phrases_file"]
        )
        print("complete ner")

    def build_predictors(self):
        """Build prediction maps after NER"""
        self.predictor.build_from_ner(self.config["ner_phrases_file"])
        self.predictor.save_predictors(
            self.config["word_pred_file"],
            self.config["char_pred_file"]
        )
        print("Prediction maps built")