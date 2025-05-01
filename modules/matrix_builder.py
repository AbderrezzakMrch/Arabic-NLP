# matrix_builder.py
import json
from collections import defaultdict
import os


class WordLevelMatrixBuilder:
    def __init__(self, config):
        self.config = config
        self.word_probs = defaultdict(dict)
        self.word_counts = defaultdict(lambda: defaultdict(int))
        self.total_transitions = defaultdict(int)
        self.stop_words = set()

    def load_stop_words(self):
        """Load stop words from file"""
        with open(self.config["stop_words_file"], 'r', encoding='utf-8') as f:
            self.stop_words = {line.strip() for line in f if line.strip()}

    def load_vocabulary(self):
        """Load the final vocabulary"""
        with open(self.config["Vocab_Final"], 'r', encoding='utf-8') as f:
            # Filter out stopwords from vocabulary
            vocab_data = json.load(f)
            self.vocab = {word['Word'] for word in vocab_data
                         if word['Word'] not in self.stop_words}

    def load_phrases(self):
        """Load processed phrases and filter stopwords"""
        with open(self.config["phrases_file"], 'r', encoding='utf-8') as f:
            phrases = json.load(f)
            # Filter stopwords from each phrase
            self.phrases = []
            for phrase in phrases:
                filtered_phrase = [word for word in phrase.split()
                                 if word not in self.stop_words]
                if len(filtered_phrase) > 1:  # Only keep phrases with at least 2 words
                    self.phrases.append(' '.join(filtered_phrase))

    def build_from_phrases(self):
        """Build word probability matrix from phrases (already filtered)"""
        # Count word pairs only for vocabulary words
        for phrase in self.phrases:
            words = phrase.split()
            for i in range(len(words) - 1):
                current = words[i]
                next_word = words[i + 1]
                if current in self.vocab and next_word in self.vocab:
                    self.word_counts[current][next_word] += 1
                    self.total_transitions[current] += 1

        # Calculate probabilities (P(next_word|current_word))
        for word, next_words in self.word_counts.items():
            total = self.total_transitions[word]
            self.word_probs[word] = {w: count / total for w, count in next_words.items()}

    def save_matrix(self):
        """Save word probability matrix in array-wrapped format"""
        os.makedirs(os.path.dirname(self.config["word_matrix_file"]), exist_ok=True)
        with open(self.config["word_matrix_file"], 'w', encoding='utf-8') as f:
            json.dump(
                self.word_probs,
                f,
                ensure_ascii=False,
                indent=2
            )


class CharLevelMatrixBuilder:
    def __init__(self, config):
        self.config = config
        self.char_probs = defaultdict(dict)
        self.char_counts = defaultdict(lambda: defaultdict(int))
        self.total_char_transitions = defaultdict(int)

    def load_vocabulary(self):
        """Load character vocabulary from final words"""
        with open(self.config["Vocab_Final"], 'r', encoding='utf-8') as f:
            words = {word['Word'] for word in json.load(f)}
            self.chars = set(char for word in words for char in word)

    def build_from_vocabulary(self):
        """Build character probability matrix"""
        with open(self.config["Vocab_Final"], 'r', encoding='utf-8') as f:
            for word in json.load(f):
                word_text = word['Word']
                for i in range(len(word_text) - 1):
                    current = word_text[i]
                    next_char = word_text[i + 1]
                    if current in self.chars and next_char in self.chars:
                        self.char_counts[current][next_char] += 1
                        self.total_char_transitions[current] += 1

        # Calculate probabilities (P(next_char|current_char))
        for char, next_chars in self.char_counts.items():
            total = self.total_char_transitions[char]
            self.char_probs[char] = {c: count / total for c, count in next_chars.items()}

    def save_matrix(self):
        """Save character probability matrix in array-wrapped format"""
        os.makedirs(os.path.dirname(self.config["char_matrix_file"]), exist_ok=True)
        with open(self.config["char_matrix_file"], 'w', encoding='utf-8') as f:
            json.dump(
                self.char_probs,
                f,
                ensure_ascii=False,
                indent=2
            )