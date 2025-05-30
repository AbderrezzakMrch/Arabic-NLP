# Arabic NLP

This repository contains a Natural Language Processing (NLP) project focused on Arabic text processing. The project leverages **Qalsadi** for lemmatization and tokenization, and **NLTK** for stemming and additional text processing utilities. The goal is to provide a robust pipeline for preprocessing Arabic text, which can be used for downstream NLP tasks such as sentiment analysis, text classification, and machine translation.

## Features

- **Tokenization**: Splitting Arabic text into words or subwords using Qalsadi.
- **Lemmatization**: Converting Arabic words to their base or dictionary forms using Qalsadi.
- **Stemming**: Reducing Arabic words to their root forms using NLTK's ISRI Stemmer.
- **Text Normalization**: Removing diacritics (Tashkeel) and unifying Arabic characters.

## Libraries Used

- **[Qalsadi](https://github.com/linuxscout/qalsadi)**: For Arabic lemmatization and tokenization.
- **[NLTK](https://www.nltk.org/)**: For stemming and additional text processing utilities.

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/AbderrezzakMrch/Arabic-NLP.git
   cd Arabic-NLP
