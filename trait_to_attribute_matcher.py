import spacy

nlp = spacy.load("en_core_web_sm")

def match_traits_to_attribute(attribute_features, trait_features, non_stemmed_features):
    result_trait_list = []
    for tfeature in trait_features:
        if len(tfeature['2']) == 0:
            continue
        expected_count = len(tfeature['2'][0])
        actual_count = 0
        for word in attribute_features:
            if word in tfeature['2'][0]:
                actual_count += 1
            if actual_count == expected_count:
                result_trait_list.append(tfeature['1'][0])
                break

    traits_from_unstemmed_features = None
    if non_stemmed_features is not None:
        traits_from_unstemmed_features = find_similar_traits(non_stemmed_features, trait_features)

    return result_trait_list if traits_from_unstemmed_features is None else list(set(result_trait_list).union(set(traits_from_unstemmed_features)))

def find_similar_traits(nonstemmed_attribute_features, trait_features):
    result_trait_list = []
    for tfeature in trait_features:
        if len(tfeature['2']) == 0:
            continue
        for word in nonstemmed_attribute_features:
            #print (word, tfeature['2'][1])
            if nlp(word).vector_norm and nlp(tfeature['2'][1]).vector_norm:
                if nlp(word).similarity(nlp(tfeature['2'][1])) > 0.6:
                    result_trait_list.append(tfeature['1'][0])
                    break
    print ("similar")
    print (result_trait_list)
    return result_trait_list