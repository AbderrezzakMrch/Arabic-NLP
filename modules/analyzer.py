def calculate_word_frequencies(words):
    """
    Calculate word frequencies.
    """
    frequency_dict = {}
    for word in words:
        frequency_dict[word] = frequency_dict.get(word, 0) + 1
    return frequency_dict

def prepare_word_frequency_data(word_freq, total_tokens):
    """
    Prepare word frequency data for JSON output.
    """
    word_frequence = []
    for id_number, (word, count) in enumerate(word_freq.items()):
        word_frequence.append({
            'ID': id_number,
            'Word': word,
            'Apperance': count,
            'Frequency': count / total_tokens
        })
    return word_frequence
