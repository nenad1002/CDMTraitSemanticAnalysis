# This file contains NLP utility methods.
from nltk.corpus import stopwords
from string import punctuation

custom_stop_words = set(stopwords.words('english') + list(punctuation))


# Removes stop words from a tokenized sentence.
def remove_stop_words(sent):
    for word in sent:
        if word in custom_stop_words:
            sent.remove(word)

    return sent


def convert_to_lower_case(features):
    result = []
    for feature in features:
        result.append(feature.lower())

    return result