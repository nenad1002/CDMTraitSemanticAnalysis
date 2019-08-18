import benchmark_runner
import trait_extractor
import attribute_extractor
from nltk.stem import WordNetLemmatizer
from nltk.stem import LancasterStemmer, SnowballStemmer
from nltk.probability import FreqDist
import description_analyzer
import trait_analyzer
import attribute_name_analyzer
import spacy

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


def match_traits_to_attribute(attribute_features, trait_features):
    result_trait_list = []
    for tfeature in trait_features:
        if len(tfeature['2']) == 0:
            continue
        expected_count = len(tfeature['2'])
        actual_count = 0
        for word in attribute_features:
            if word in tfeature['2']:
                actual_count += 1
            if actual_count == expected_count:
                result_trait_list.append(tfeature['1'][0])
                break

    return set(result_trait_list)

def analyze_attributes_in_entities(paths, expected_traits = None):
    attributes = attribute_extractor.extract_attributes(paths)


    outputDic = {}

    for attribute in attributes:
        stem_feature = attribute_name_analyzer.lemma_and_stem_attribute(lancester, wordnet_lemmatizer, attribute)
        if attribute[1] != '':
            sentence_feature = description_analyzer.lemma_and_stem_sentence_spacy(lancester, attribute[1], False)
        else:
            sentence_feature = []

        print()
        print("------- attribute -------")
        print(attribute[0])
        print('------- traits -------')

        # Connect attribute and sentence features and remove duplicates.
        stem_feature = list(dict.fromkeys(stem_feature + sentence_feature))

        result_trait_set = match_traits_to_attribute(stem_feature, stem_traits)

        print (result_trait_set)
        print ('----------------')
        print ()

        outputDic[attribute[0]] = result_trait_set

    if expected_traits is not None:
        benchmark_dict = benchmark_runner.extract_example_data(expected_traits)
        print("The Jaccard index of similarity for this example is", benchmark_runner.measure_similarity(outputDic, benchmark_dict))

def analyze_single_attribute(attribute, description):
    attribute = [attribute, description]
    stem_feature = attribute_name_analyzer.lemma_and_stem_attribute(lancester, wordnet_lemmatizer, attribute)
    if description != '':
        sentence_feature = description_analyzer.lemma_and_stem_sentence_spacy(lancester, attribute[1], True)
    else:
        sentence_feature = []

    # Connect attribute and sentence features and remove duplicates.
    stem_feature = list(dict.fromkeys(stem_feature + sentence_feature))
    print()
    print("------- attribute ------")
    print(attribute[0])
    print('------- traits -----------')

    result_trait_set = match_traits_to_attribute(stem_feature, stem_traits)
    print (result_trait_set)
    print ('-------------')
    print ()

def main(whetherToAnalyzeSchema):
    if whetherToAnalyzeSchema:
        analyze_attributes_in_entities(['CDM.SchemaDocuments/core/applicationCommon/Account.cdm.json'], 'handwritten-examples/Account.trait.json')
    else:
        attribute = input("Enter attribute name: ")
        description = input("Enter description: ")
        analyze_single_attribute(attribute, description)

if __name__ == "__main__":
    main(ANALYZE_ATTRIBUTES_FROM_SCHEMA)
