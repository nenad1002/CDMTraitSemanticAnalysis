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

    return set(result_trait_list)

def find_similar_traits(nonstemmed_attribute_features, trait_features):
    result_trait_list = []
    for tfeature in trait_features:
        if len(tfeature['2']) == 0:
            continue
        for word in nonstemmed_attribute_features:
            #print (word, tfeature['2'][1])
            if nlp(word).vector_norm and nlp(tfeature['2'][1]).vector_norm:
                if nlp(word).similarity(nlp(tfeature['2'][1])) > 0.9:
                    result_trait_list.append(tfeature['1'][0])
                    break
    print (result_trait_list)
    return result_trait_list