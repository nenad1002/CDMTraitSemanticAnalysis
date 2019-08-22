from nltk.tokenize import RegexpTokenizer

class TraitAnalyzer:
    '''The class that does preprocessing on the traits to ensure all features are properly extracted by
    doing stemming, optional lemming and removing noisy features.
    '''

    camel_case_tokenizer = None

    def __init__(self):
        # Needed to be able to tokenize traits that have multiple words in a feature.
        camel_case_tokenizer = RegexpTokenizer('([A-Z]?[a-z]+)')

    # Used only when we want to break features in traits that contain multiple words - so far it produces too much noise.
    # Feel free to comment it out if want to use.
    # def lemma_and_stem_trait_helper(self, stemmer, lemmatizer, trait, index):
    #    trait_features = self.camel_case_tokenizer.tokenize(trait[1][index])
    #    trait_features = nlp_utility.convert_to_lower_case(trait_features)
    #    feature_words = nlp_utility.remove_stop_words(trait_features)
    #    result = []
    #    for feature in feature_words:
    #        stem = stemmer.stem(feature)
    #        result.append(stem)
    #        return result


    def stem_traits(self, trait_list, stemmer, lemmatizer, noise_manager):
        '''
        It does stemming on the traits features.
        :param trait_list: The trait list.
        :param stemmer: The stemmer.
        :param lemmatizer: The lemmatizer, a user can optionally add code which uses lemmatizer.
        :param noise_manager: The noise manager.
        :return: The list objects containing the stemmed/not stemmed features and the original traits.
        '''
        result = []

        # Find trait features which might produce too much noise.
        noise_manager.generate_commonly_occured_noise(trait_list)

        for trait in trait_list:
            for i in range(len(trait[1]) - 1, -1, -1):
                # Do stemming on the trait feature, optionally lemmatization can be done as well by using the lemmatizer.
                # Optionally, a user can try to see can the feature be broken down as well into separate words by calling the helper method.
                stemmed_word = [stemmer.stem(trait[1][i])]
                non_stemmed_word = trait[1][i]

                # Creating an object, so later we can extract out both traits and stemmed/not stemmed features.
                obj = {'1' : trait, '2': (stemmed_word, non_stemmed_word)}

                if i == len(trait[1]) - 1 or not noise_manager.is_generating_too_much_noise(trait[1][i]):
                    result.append(obj)

        return result