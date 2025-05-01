import re

class TextProcessor:
    def __init__(self):
        # Arabic-specific patterns
        self.tashkeel = re.compile(r'[\u064b-\u065f\u0670]')
        self.special_chars = re.compile(r'[\[\(\{](.*?)[\]\)\}]')
        self.non_arabic = re.compile(r'[^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF ]')
        self.sentence_enders = re.compile(r'(?<=[.؟!۔,،])\s+')

        # Corpus-specific patterns
        self.dash_pattern = re.compile(r'^ـ+\s*|\s*ـ+$')
        self.page_ref_pattern = re.compile(r'\bص\s*ـ*\s*\d*\b')
        self.corruption_pattern = re.compile(r'[ـ_çà)§/;,،]')
        self.multi_space = re.compile(r'\s{2,}')

    def normalize_arabic(self, text):
        text = self.tashkeel.sub('', text)

        text = re.sub(r'[إأآٱا]', 'ا', text)
        text = re.sub(r'ى', 'ي', text)
        text = re.sub(r'ؤ', 'و', text)
        text = re.sub(r'ئ', 'ي', text)
        text = re.sub(r'ة', 'ه', text)

        return text

    def split_into_phrases(self, text):
        if not isinstance(text, str):
            raise ValueError("Expected input to be a string.")

        text = self.normalize_arabic(text)
        all_phrases = []

        # Split text based on sentence-ending punctuation
        main_phrases = [p.strip() for p in self.sentence_enders.split(text) if p.strip()]

        for phrase in main_phrases:
            phrase = self._clean_corpus_specific(phrase)
            clean_phrase = self._process_special_content(phrase, all_phrases)
            clean_phrase = self._final_clean(clean_phrase)

            if clean_phrase and len(clean_phrase.split()) >= 2:
                if not re.search(r'[.؟!]$', clean_phrase):
                    clean_phrase += '.'
                all_phrases.append(clean_phrase)

        return all_phrases

    def _process_special_content(self, phrase, all_phrases):
        clean_phrase = phrase
        for match in self.special_chars.finditer(phrase):
            for group in match.groups():
                if group:
                    cleaned_content = self._clean_corpus_specific(group.strip())
                    cleaned_content = self._final_clean(cleaned_content)
                    if cleaned_content and len(cleaned_content.split()) >= 2:
                        if not re.search(r'[.؟!]$', cleaned_content):
                            cleaned_content += '.'
                        all_phrases.append(cleaned_content)
                    clean_phrase = clean_phrase.replace(match.group(0), "")
        return clean_phrase

    def _clean_corpus_specific(self, text):
        text = self.dash_pattern.sub('', text)
        text = self.page_ref_pattern.sub('', text)
        text = self.corruption_pattern.sub('', text)
        text = self.multi_space.sub(' ', text).strip()
        return text

    def _final_clean(self, phrase):
        phrase = self.non_arabic.sub('', phrase)
        phrase = re.sub(r'\d+', '', phrase)
        phrase = re.sub(r'[؟!.,،;:§_\-/|\"\'<>]', '', phrase)
        phrase = re.sub(r'\s+', ' ', phrase).strip()
        return phrase
