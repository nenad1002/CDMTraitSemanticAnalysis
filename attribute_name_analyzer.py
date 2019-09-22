import nlp_utility
from nltk.tokenize import RegexpTokenizer

class AttributeNameAnalyzer:
    def __init__(self):
        self.camel_case_tokenizer = RegexpTokenizer('([A-Z]?[a-z]+)')


    def stem_attribute(self, stemmer, lemmatizer, attribute):
        '''
        Does stemming of the attributes.
        :param stemmer: The stemmer.
        :param lemmatizer: The lemmatizer, it is not used, but optionally it can be turned on by a user.
        :param attribute: The attribute.
        :return: The list of stemmed/non-stemmed feature pairs.
        '''

        # First tokenize the attribute.
        features_list = self.camel_case_tokenizer.tokenize(attribute[0])
        features_list = nlp_utility.convert_to_lower_case(features_list)

        # Remove the user defined stop words.
        feature_words = nlp_utility.remove_stop_words(features_list)

        result = []
        for word in feature_words:
            stem = stemmer.stem(word)
            result.append(stem)

        return result, feature_words