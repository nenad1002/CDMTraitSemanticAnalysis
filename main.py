import nltk

nltk.download('averaged_perceptron_tagger')

import benchmark_runner
import trait_extractor
import attribute_extractor
import noise_manager
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, SnowballStemmer
from nltk.tokenize import word_tokenize, RegexpTokenizer
from string import punctuation
from nltk import pos_tag
from nltk.probability import FreqDist

custom_stop_words = set(stopwords.words('english') + list(punctuation))

print (custom_stop_words)
# print(custom_stop_words)

# Aggresive stemming preferred.
# lancester = SnowballStemmer('english')
lancester = LancasterStemmer()

wordnet_lemmatizer = WordNetLemmatizer()

camel_case_tokenizer = RegexpTokenizer('([A-Z]?[a-z]+)')


def lemma_and_stem_trait_helper(trait, index):
    trait_features = camel_case_tokenizer.tokenize(trait[1][index])

    newList = []

    for feature in trait_features:
        newList.append(feature.lower())

    trait_features = newList

    if trait[0] == 'means.calendar.dayOfWeek':
        print ('aaaaa', trait_features)
    feature_words = remove_stop_words(trait_features)

    result = []

    for feature in feature_words:
        lemma = wordnet_lemmatizer.lemmatize(feature)
        stem = lancester.stem(lemma)
        result.append(stem)

    return result

def lemmaAndStemTraits(trait_list):
    result = []
    for trait in trait_list:
        for i in range(len(trait[1]) - 1, -1, -1):
            lemma = wordnet_lemmatizer.lemmatize((trait[1][i]))
            stem = lancester.stem(lemma)
            # If a user wants to break trait words as well.
            #new_stems = lemma_and_stem_trait_helper(trait, i)
            new_stems = [stem]
            obj = {'1' : trait, '2': new_stems}
            print (obj)
            if i == len(trait[1]) - 1 or not noise_manager.is_generating_too_much_noise(trait[1][i]):
                result.append(obj)

    return result


def remove_stop_words(sent):
    for word in sent:
        if word in custom_stop_words:
            sent.remove(word)
    return sent


# TODO Will be used for description, still need to figure out how will I weight words in sentences.
def lemmaAndStemSentence(sent):
    sentence_words = word_tokenize(sent)
    pos = pos_tag(sentence_words)
    sentence_words = remove_stop_words(sentence_words)

    result = []
    for word in pos:
        if word[1] == 'NN' or word[1] == 'NNS' or word[1] == 'NNP':
            stem = lancester.stem(word[0])
            result.append(stem)

    return result


def lemmaAndStemAttribute(features_list):
    [feature.lower() for feature in features_list]
    feature_words = remove_stop_words(features_list)

    result = []
    for word in feature_words:
        lemma = wordnet_lemmatizer.lemmatize(word)
        stem = lancester.stem(lemma)
        result.append(stem)

    return result


trait_files = ['meanings.cdm.json', 'foundations.cdm.json', 'primitives.cdm.json']

trait_list = trait_extractor.extract_traits('CDM.SchemaDocuments/', trait_files)

attributes = attribute_extractor.extract_attributes(['CDM.SchemaDocuments/core/applicationCommon/Account.cdm.json'])

camel_case_tokenizer = RegexpTokenizer('([A-Z]?[a-z]+)')

noise_manager.find_commonly_occured_noise(trait_list)

stem_traits = lemmaAndStemTraits(trait_list)

# for ss in wn.synsets('credit'):
#    for hyper in ss.hypernyms():
#        print (ss, hyper)

outputDic = {}

for attribute in attributes:
    features = camel_case_tokenizer.tokenize(attribute[0])
    stem_feature = lemmaAndStemAttribute(features)
    if attribute[1] != '':
        sentence_feature = lemmaAndStemSentence(attribute[1])
    else:
        sentence_feature = []

    # Connect attribute and sentence features and remove duplicates.
    stem_feature = list(dict.fromkeys(stem_feature + sentence_feature))

    print()
    print("-------")
    print(attribute)
    print('-------')
    outputTraitList = []
    for word2 in stem_traits:
        if len(word2['2']) == 0:
            continue
        expected_count = len(word2['2'])
        actual_count = 0
        if word2['1'][0] == 'means.calendar.dayOfWeek':
            print ('means.calendar.dayOfWeek', attribute[0], stem_feature)
        for word in stem_feature:
            if word in word2['2']:
                actual_count += 1
            if actual_count == expected_count:
                outputTraitList.append(word2['1'][0])
                print(word2['1'][0])
                print(stem_feature)
                print("word2", word2['2'], len(word2['2']))
                break

    outputTraitSet = set(outputTraitList)
    outputDic[attribute[0]] = outputTraitSet

# print (outputDic)

benchmark_dict = benchmark_runner.extract_example_data('handwritten-examples/Account.trait.json')

print(benchmark_dict)

print(benchmark_runner.measure_similarity(outputDic, benchmark_dict))

print(noise_manager.noise_features)


