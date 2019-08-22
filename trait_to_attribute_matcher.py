import spacy


class TraitToAttributeMatcher:
    nlp = None

    is_similar_word_processing = False  # Type: boolean

    precision = 0

    def __init__(self, is_similar_word_processing=False, precision = 0):
        '''
        Creates a new instance of TraitToAttributeMatcher.
        :param is_similar_word_processing: The flag that denotes whether we want to use the vector based similariy search.
        :param precision: The minimum cosine similarity between two features to consider it similar.
        '''
        self.is_similar_word_processing = is_similar_word_processing
        if is_similar_word_processing:
            # Load medium or big corpus of english words.
            self.nlp = spacy.load("en_core_web_sm")
            self.precision = precision

    def match_traits_to_attribute(self, attribute_features, trait_features, non_stemmed_features=None):
        '''
        It matches trait features to the attribute features.
        :param attribute_features: The list of attribute features.
        :param trait_features: The list of trait (stem) features.
        :param non_stemmed_features: The list of trait (non-stem) features.
        :return: A list of traits that match the attribute features/
        '''
        result_trait_list = []

        for tfeature in trait_features:
            # There is no feature, happens for some weirdly defined traits.
            if len(tfeature['2']) == 0:
                continue

            # Expected and actual count are here since some feature might consist of the set of words
            # and we want to match all the words (usually it is just one word).
            expected_count = len(tfeature['2'][0])
            actual_count = 0
            for word in attribute_features:
                if word in tfeature['2'][0]:
                    actual_count += 1
                if actual_count == expected_count:
                    result_trait_list.append(tfeature['1'][0])
                    break

        traits_from_unstemmed_features = None

        # Do additional processing only if a user sets the flag which allows to find similar trait features.
        if self.is_similar_word_processing and non_stemmed_features is not None:
            traits_from_unstemmed_features = self.find_similar_traits(non_stemmed_features, trait_features)

        return result_trait_list if traits_from_unstemmed_features is None else list(
            set(result_trait_list).union(set(traits_from_unstemmed_features)))


    def find_similar_traits(self, nonstemmed_attribute_features, trait_features):
        '''
        Searches for the list of attribute features which might be similar enough to some of the trait features.
        :param nonstemmed_attribute_features: The list of attribute features (non-stemmed)
        :param trait_features: The list of trait features.
        :return:
        '''
        result_trait_list = []
        for tfeature in trait_features:
            if len(tfeature['2']) == 0:
                continue
            for word in nonstemmed_attribute_features:

                # Find the vector norms of each word and then calculate their cosine similarity.
                if self.nlp(word).vector_norm and self.nlp(tfeature['2'][1]).vector_norm:
                    if self.nlp(word).similarity(self.nlp(tfeature['2'][1])) > self.precision:
                        result_trait_list.append(tfeature['1'][0])
                        break

        return result_trait_list
