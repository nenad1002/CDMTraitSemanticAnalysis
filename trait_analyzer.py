from nltk.tokenize import RegexpTokenizer
import nlp_utility
import noise_manager

# Needed to be able to tokenize traits that have multiple words in a feature.
camel_case_tokenizer = RegexpTokenizer('([A-Z]?[a-z]+)')

# Used only when we want to break features in traits that contain multiple words - so far it produces too much noise.
def lemma_and_stem_trait_helper(stemmer, lemmatizer, trait, index):
    trait_features = camel_case_tokenizer.tokenize(trait[1][index])

    trait_features = nlp_utility.convert_to_lower_case(trait_features)

    feature_words = nlp_utility.remove_stop_words(trait_features)

    result = []

    for feature in feature_words:
        #lemma = lemmatizer.lemmatize(feature)
        stem = stemmer.stem(feature)
        result.append(stem)

    return result


def lemma_and_stem_traits(stemmer, lemmatizer, trait_list):
    result = []

    # Find trait features which might produce too much noise.
    noise_manager.find_commonly_occured_noise(trait_list)

    for trait in trait_list:
        for i in range(len(trait[1]) - 1, -1, -1):
            lemma = lemmatizer.lemmatize((trait[1][i]))
            stem = stemmer.stem(lemma)
            non_stemmed_word = trait[1][i]

            # If a user wants to break trait words as well.
            #new_stems = lemma_and_stem_trait_helper(trait, i)
            new_stems = [stem]
            obj = {'1' : trait, '2': (new_stems, non_stemmed_word)}
            if i == len(trait[1]) - 1 or not noise_manager.is_generating_too_much_noise(trait[1][i]):
                result.append(obj)

    return result