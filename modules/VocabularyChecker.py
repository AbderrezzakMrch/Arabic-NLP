
import nltk
from nltk.stem.isri import ISRIStemmer
from farasa.segmenter import FarasaSegmenter
from farasa.ner import FarasaNamedEntityRecognizer



import stanza
class VocabularyChecker:
    def __init__(self):
        # Initialize processing tools
        self.nltk_stemmer = ISRIStemmer()
        #self.farasa_segmenter = FarasaSegmenter()
        #self.farasa_ner = FarasaNamedEntityRecognizer()

        self.nlp = stanza.Pipeline('ar', processors='tokenize,mwt,pos,lemma,ner')

    def is_stop_word(self, word,stopwords):
        """Check if word is in stop words"""
        return word in stopwords

    def is_in_dictionary(self, word,dictionary_words):
        """Check if word exists in dictionary"""
        return word in dictionary_words

    def has_stemming(self, word):
        """Check if word can be stemmed"""
        try:
            stemmed = self.nltk_stemmer.stem(word)
            if(stemmed and stemmed != word and len(stemmed) > 1):
                print(f"Original: {word} | Stemmed: {stemmed}")
            return stemmed and stemmed != word and len(stemmed) > 1
        except Exception:
            return False

    def has_lemmatization(self, word):
        """Check if word can be lemmatized using Stanza"""
        if len(word) < 2:  # Skip very short words
            return False

        try:
            doc = self.nlp(word)
            if not doc.sentences:
                return False

            # Get lemma from first word in first sentence²
            lemma = doc.sentences[0].words[0].lemma if doc.sentences[0].words else None

            if lemma and lemma != word:
                print(f"Original: {word} | Lemmatized: {lemma}")
                return True
            return False

        except Exception as e:
            print(f"Lemmatization error for '{word}': {str(e)}")
            return False
    '''
    def is_named_entity(self, word):
        """Check if word is a named entity"""
        try:
            ner_result = self.farasa_ner.recognize(word)
            if '/' in ner_result:
                _, entity_tag = ner_result.split('/')
                if(entity_tag not in ('O', 'UNK')):
                    print(f"✅ Accepted: {word} (NER tag: {entity_tag})")
                return entity_tag not in ('O', 'UNK')
            return False
        except Exception:
            return False
        '''


    def is_named_entity(self, word):
        """Check if word is a named entity"""
        try:
            doc = self.nlp(word)
            if doc.sentences and doc.sentences[0].ents:
                ent_type = doc.sentences[0].ents[0].type
                print(f"✅ Accepted: {word} (NER tag: {ent_type})")
                return True
            return False
        except Exception:
            return False