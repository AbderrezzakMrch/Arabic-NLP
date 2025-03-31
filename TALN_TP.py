import json
import re
from pypdf import PdfReader  # PyPDF2



# Read the stop words file
def read_stop_words(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        stop_words = set(file.read().splitlines())
    return stop_words


# Read text from a PDF file using PyPDF2
def read_pdf(file_path):
    text = ""
    # Create a PDF reader object
    reader = PdfReader(file_path)
    # Iterate through each page
    for page in reader.pages:
        # Extract text from the page
        text += page.extract_text()
    return text


# Function to check if a word is in Arabic
def is_arabic(word):
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u061B\u061F\u0640\u0660-\u0669\u066A\u066B\u066C\u066D\u067E\u0686\u06AF\u06A4\u06A9\u06CC\u06F0-\u06F9]+')
    return bool(arabic_pattern.fullmatch(word))


# Tokenize the corpus
def tokenize(text):
    # Split by whitespace
    words = text.split()
    # Remove punctuation, filter out words containing numbers, and keep only Arabic words
    words = [word.strip('.,!؟؛،()[]{}"\'') for word in words
             if not any(char.isdigit() for char in word) and is_arabic(word)]
    return words


# Function to calculate word frequencies
def calculate_word_frequencies(words, stop_words):
    frequency_dict = {}
    for word in words:
        if word not in stop_words:
            if word in frequency_dict:
                frequency_dict[word] += 1
            else:
                frequency_dict[word] = 1
    return frequency_dict


# Function to save in a JSON file
def save_in_json(data, output_file):
    with open(output_file, 'w', encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# Main code
def main():
    # Read stop words
    stop_words = read_stop_words("stop_arabic.txt")

    # Read text from a PDF file
    corpus = read_pdf("المقاومات الشعبية في الجزائر وتونس دراسة تاريخية مقارنة.pdf")  # Replace with your PDF file path

    # Tokenize the text
    tokens = tokenize(corpus)

    # Calculate word frequencies
    word_freq = calculate_word_frequencies(tokens, stop_words)

    # Convert word frequencies to a list of tuples
    vocabulary = list(word_freq.items())

    # Print statistics
    print("Total Tokens:", len(tokens))
    print("Unique Words:", len(vocabulary))

    # Prepare word frequency data for JSON
    word_frequence = []
    id_number = 0
    for word, count in vocabulary:
        word_frequence.append({
            'ID': id_number,
            'Word': word,
            'Apperance': count,
            'Frequency': count / len(tokens)
        })
        id_number += 1

    # Save tokens and word frequencies to JSON files
    save_in_json(dict(enumerate(tokens)), "tokens.json")
    save_in_json(word_frequence, "word_freq.json")

    print("Word frequencies saved in -> word_freq.json")


if __name__ == "__main__":
    main()



