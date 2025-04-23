import json
from collections import defaultdict


class ArabicPredictor:
    def __init__(self):
        self.word_prefix_map = defaultdict(list)
        self.char_ngrams = defaultdict(list)

    def build_from_ner(self, ner_results_file):
        """Handle both list and dictionary NER outputs"""
        with open(ner_results_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Case 1: List format (direct entities)
        if isinstance(data, list):
            self._process_entities(data)
        # Case 2: Dictionary format (structured output)
        elif 'entities' in data:
            for entity_group in data['entities']:
                self._process_entities(entity_group.values())

    def _process_entities(self, entities):
        """Process a list of entity words"""
        for word in entities:
            if isinstance(word, str):
                # Word-level predictions
                for i in range(2, len(word)):
                    self.word_prefix_map[word[:i]].append(word)

                # Character-level predictions
                for i in range(len(word) - 1):
                    self.char_ngrams[word[i]].append(word[i + 1])

    def save_predictors(self, word_pred_file, char_pred_file):
        """Compact JSON saving"""
        with open(word_pred_file, 'w', encoding='utf-8') as f:
            json.dump(
                {k: list(set(v)) for k, v in self.word_prefix_map.items()},
                f,
                ensure_ascii=False,
                indent=2
            )

        with open(char_pred_file, 'w', encoding='utf-8') as f:
            json.dump(
                {k: list(set(v)) for k, v in self.char_ngrams.items()},
                f,
                ensure_ascii=False,
                indent=2
            )