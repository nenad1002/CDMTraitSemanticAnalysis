import benchmark_runner
import nlp_utility
import trait_extractor
import attribute_extractor
from nltk.stem import WordNetLemmatizer
from nltk.stem import LancasterStemmer, SnowballStemmer
from nltk.probability import FreqDist
import description_analyzer
import trait_analyzer
import attribute_name_analyzer
import spacy
import trait_to_attribute_matcher

# Change this to false if you want to analyze a single attribute,
# otherwise specify path to the entity you want to analyze.
ANALYZE_ATTRIBUTES_FROM_SCHEMA = True

# Aggresive stemming preferred.
# lancester = SnowballStemmer('english')
lancester = LancasterStemmer()


# Use wordnet for lemmas.
wordnet_lemmatizer = WordNetLemmatizer()


trait_files = ['meanings.cdm.json', 'foundations.cdm.json', 'primitives.cdm.json']

trait_list = trait_extractor.extract_traits('CDM.SchemaDocuments/', trait_files)

stem_traits = trait_analyzer.lemma_and_stem_traits(lancester, wordnet_lemmatizer, trait_list)


def analyze_attributes_in_entities(paths, expected_traits = None):
    attributes = attribute_extractor.extract_attributes(paths)

    outputDic = {}

    for attribute in attributes:
        attribute_feature = attribute_name_analyzer.lemma_and_stem_attribute(lancester, wordnet_lemmatizer, attribute)
        if attribute[1] != '':
            sentence_features = description_analyzer.lemma_and_stem_sentence_spacy(lancester, attribute[1], False)
        else:
            sentence_features = []

        print()
        print("------- attribute -------")
        print(attribute[0])
        print('------- traits -------')

        # We have some data
        if (len(sentence_features) > 0):
            stemmed_sentence_features = sentence_features[0]
            unstemmed_sentence_features = sentence_features[1]
        else:
            stemmed_sentence_features = []
            unstemmed_sentence_features = []

        if len(attribute_feature) > 0:
            stemmed_attribute_feature = attribute_feature[0]
            unstemmed_attribute_feature = attribute_feature[1]

        # Connect attribute and sentence features and remove duplicates.
        stemmed_features = list(dict.fromkeys(stemmed_attribute_feature + stemmed_sentence_features))
        unstemmed_features = list(dict.fromkeys(unstemmed_attribute_feature + unstemmed_sentence_features))

        # We don't want unstemmed features since similarity check could take too long. Change None to unstemmed_features
        # if similarity check is something that is preferred to do.
        result_trait_set_from_attribute = trait_to_attribute_matcher.match_traits_to_attribute(stemmed_attribute_feature, stem_traits, None)
        result_trait_set_from_dict = trait_to_attribute_matcher.match_traits_to_attribute(stemmed_sentence_features, stem_traits, None)

        result_traits = nlp_utility.define_proper_order(result_trait_set_from_attribute, result_trait_set_from_dict)
        print(result_traits)
        print ('----------------')
        print ()

        outputDic[attribute[0]] = set(result_traits)

    if expected_traits is not None:
        benchmark_dict = benchmark_runner.extract_example_data(expected_traits)
        print("The Jaccard index of similarity for this example is", benchmark_runner.measure_similarity(outputDic, benchmark_dict))

def analyze_single_attribute(attribute, description):
    attribute = [attribute, description]
    attribute_feature = attribute_name_analyzer.lemma_and_stem_attribute(lancester, wordnet_lemmatizer, attribute)
    if description != '':
        sentence_features = description_analyzer.lemma_and_stem_sentence_spacy(lancester, attribute[1], False)
    else:
        sentence_features = []

    if (len(sentence_features) > 0):
        stemmed_sentence_features = sentence_features[0]
        unstemmed_sentence_features = sentence_features[1]
    else:
        stemmed_sentence_features = []
        unstemmed_sentence_features = []

    if len(attribute_feature) > 0:
        stemmed_attribute_feature = attribute_feature[0]
        unstemmed_attribute_feature = attribute_feature[1]

    print()
    print("------- attribute ------")
    print(attribute[0])
    print('------- traits -----------')

    result_trait_set_from_attributes = trait_to_attribute_matcher.match_traits_to_attribute(stemmed_attribute_feature, stem_traits,
                                                                            None)
    result_trait_set_from_desc = trait_to_attribute_matcher.match_traits_to_attribute(stemmed_sentence_features, stem_traits, None)

    result_traits = nlp_utility.define_proper_order(result_trait_set_from_attributes, result_trait_set_from_desc)
    print (result_traits)

    #print (result_trait_set_from_desc)

    #result_trait_set_from_attributes = trait_to_attribute_matcher.match_traits_to_attribute(stem_feature, stem_traits)
    #result_trait_set_from_desc = trait_to_attribute_matcher.match_traits_to_attribute(stem_feature, stem_traits)
    #print (list(dict.fromkeys(result_trait_set_from_attributes + result_trait_set_from_desc)))
    print ('-------------')
    print ()

def main(whetherToAnalyzeSchema):

    if whetherToAnalyzeSchema:
        analyze_attributes_in_entities(['CDM.SchemaDocuments/core/applicationCommon/Account.cdm.json'], 'handwritten-examples/Account.trait.json')
    else:
        while (True):
            attribute = input("Enter attribute name: ")
            description = input("Enter description: ")
            analyze_single_attribute(attribute, description)

if __name__ == "__main__":
    main(ANALYZE_ATTRIBUTES_FROM_SCHEMA)
