'''
This file contains NLP utility methods.
'''

from nltk.corpus import stopwords
from string import punctuation

additional_stop_words = ['it', 'he', 'she', 'we', 'this']
custom_stop_words = set(stopwords.words('english') + list(punctuation) + additional_stop_words)


#
def remove_stop_words(sent):
    '''
    Removes stop words from a tokenized sentence.
    :param sent: The sentence.
    :return: The sentence without the stop words.
    '''
    for word in sent:
        if word in custom_stop_words:
            sent.remove(word)

    return sent


def convert_to_lower_case(features):
    '''
    Converts all features into lower case.
    :param features: The features.
    :return: The lower case features.
    '''
    result = []
    for feature in features:
        result.append(feature.lower())

    return result


def define_proper_order(list1, list2):
    '''
    Once the result traits are getting merged to keep the proper ranking this method is keeping the order.
    :param list1: The first list.
    :param list2: The second list.
    :return: The merged list.
    '''
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
