import nlp_utility
from nltk.tokenize import RegexpTokenizer


camel_case_tokenizer = RegexpTokenizer('([A-Z]?[a-z]+)')


def lemma_and_stem_attribute(stemmer, lemmatizer, attribute):
    features_list = camel_case_tokenizer.tokenize(attribute[0])
    features_list = nlp_utility.convert_to_lower_case(features_list)
    feature_words = nlp_utility.remove_stop_words(features_list)

    result = []
    for word in feature_words:
        lemma = lemmatizer.lemmatize(word)
        stem = stemmer.stem(lemma)
        result.append(stem)

    return result