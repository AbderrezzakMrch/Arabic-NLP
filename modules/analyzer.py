# modules/analyzer.py

def calculate_word_frequencies(words, stop_words):
    """
    Calculate word frequencies.

    :param words: List of words.
    :param stop_words: Set of stop words to exclude.
    :return: Dictionary of word frequencies.
    """
    frequency_dict = {}
    for word in words:
        if word not in stop_words:
            frequency_dict[word] = frequency_dict.get(word, 0) + 1
    return frequency_dict


def prepare_word_frequency_data(word_freq, total_tokens):
    """
    Prepare word frequency data for JSON output.

    :param word_freq: Dictionary of word frequencies.
    :param total_tokens: Total number of tokens.
    :return: List of dictionaries containing word frequency data.
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