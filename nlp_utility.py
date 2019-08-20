# This file contains NLP utility methods.
from nltk.corpus import stopwords
from string import punctuation

additional_stop_words = ['it', 'he', 'she', 'we', 'this']
custom_stop_words = set(stopwords.words('english') + list(punctuation) + additional_stop_words)


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


"""Defines a proper order when concatanting two lists.
"""
def define_proper_order(list1, list2):
    union = set(list1).union(set(list2))
    result = []
    for it in list1:
        if it in union:
            result.append(it)
            union.remove(it)

    for it in list2:
        if it in union:
            result.append(it)
            union.remove(it)

    return result