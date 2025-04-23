from farasa.ner import FarasaNamedEntityRecognizer
import json


class ArabicNer:
    def __init__(self):
        self.named_entity_recognizer = FarasaNamedEntityRecognizer()

    def ner_text(self, text):
        named_entity_recognized = self.named_entity_recognizer.recognize(text)
        return named_entity_recognized


    def ner_phrases(self, phrases, output_file):


        ner = [self.ner_text(phrase) for phrase in phrases]

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(ner, f, ensure_ascii=False, indent=4)

        print(f"ner phrases saved to {output_file}")
        return ner