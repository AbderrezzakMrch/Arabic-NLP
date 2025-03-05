import json
import re

# read the stop words file
def read_stop_words(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        stop_words = set(file.read().splitlines())
    return stop_words


# read the corpus file
def read_corpus(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    return text

# Function to check if a word is in Arabic
def is_arabic(word):
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u061B\u061F\u0640\u0660-\u0669\u066A\u066B\u066C\u066D\u067E\u0686\u06AF\u06A4\u06A9\u06CC\u06F0-\u06F9]+')
    return bool(arabic_pattern.fullmatch(word))
# hna ndiro tokenize ll corpus ta3na
def tokenize(text):
    # Split by whitespace
    words = text.split()
    # Remove punctuation, filter out words containing numbers, and keep only Arabic words
    words = [word.strip('.,!؟؛،()[]{}"\'') for word in words
             if not any(char.isdigit() for char in word) and is_arabic(word)]
    return words

# Function to calculate word frequencies
def calculate_word_frequencies(words,stop_words):
    frequency_dict = {}
    for word in words:
        if word not in stop_words:
            if word in frequency_dict:
                frequency_dict[word] += 1
            else:
                frequency_dict[word] = 1
    return frequency_dict

#Function to save in a json file
def save_in_json(taln_dict,output_file):
    with open(output_file,'w',encoding="utf-8") as file:
        json.dump(taln_dict,file,ensure_ascii=False, indent=4)



# main code
def main():
    stop_words = read_stop_words("stop_arabic.txt")
    corpus = read_corpus("0000.txt")
    tokens = tokenize(corpus)
    word_freq = calculate_word_frequencies(tokens,stop_words)
    vocabulary = list(word_freq.items())
    print(len(tokens))
    print(len(vocabulary))
    word_frequence = []
    id_number = 0
    for i in vocabulary:
        word_frequence.append({'ID': id_number,'Word' : i[0] ,'Apperance': i[1],'Frequency': i[1]/ len(tokens)})
        id_number+= 1
    output_file = "word_freq.json"

    save_in_json(dict(enumerate(tokens)),"tokens.json")
    save_in_json(word_frequence,output_file)

    print(f"word freq was saved in -> {output_file}")

if __name__ == "__main__":
    main()
        