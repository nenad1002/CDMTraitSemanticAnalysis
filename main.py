import traitExtractor
import attributeExtractor
import noiseManager
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer
from nltk.tokenize import word_tokenize, RegexpTokenizer
from string import punctuation

custom_stop_words = set(stopwords.words('english') + list(punctuation))

print(custom_stop_words)

# Aggresive stemming preferred.
lancester = LancasterStemmer()

wordnet_lemmatizer = WordNetLemmatizer()


def lemmaAndStem(trait_list):
    result = []
    for trait in trait_list:
        # Get the canonical form of the word. TODO: measure for speed and remove if too slow.
        lemma = wordnet_lemmatizer.lemmatize(trait[1][-1])
        # Stem the canonical form of the word.
        stem = lancester.stem(lemma)
        obj = {'1': trait, '2': stem}
        result.append(obj)
        try:
            # Refactor this to use all of the features / feature extractor.
            lemma2 = wordnet_lemmatizer.lemmatize(trait[1][-2])
            stem2 = lancester.stem(lemma2)
            obj2 = {'1': trait, '2': stem2}
            # Some trait features in this stage might not be necessary and will generate too much noise.
            if not noiseManager.is_generating_too_much_noise(trait[1][-2]):
                result.append(obj2)
        except IndexError:
            print (trait)

    return result

def remove_stop_words(sent):
    for word in sent:
        if word in custom_stop_words:
            sent.remove(word)
    return sent

# TODO Will be used for description, still need to figure out how will I weight words in sentences.
def lemmaAndStemSentence(sent):
    sentence_words = word_tokenize(sent)
    sentence_words = remove_stop_words(sentence_words)

    result = []
    for word in sentence_words:
        lemma = wordnet_lemmatizer.lemmatize(word)
        stem = lancester.stem(lemma)
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

trait_list = traitExtractor.extract_traits('CDM.SchemaDocuments/', trait_files)

print (trait_list)

attributes = attributeExtractor.extract_attributes(['CDM.SchemaDocuments/core/applicationCommon/Account.cdm.json'])

camel_case_tokenizer = RegexpTokenizer('([A-Z]?[a-z]+)')

stem_traits = lemmaAndStem(trait_list)

for attribute in attributes:
    features = camel_case_tokenizer.tokenize(attribute)
    stem_sentence = lemmaAndStemAttribute(features)

    print ()
    print ("-------")
    print (attribute)
    print ('-------')
    for word in stem_sentence:
        for word2 in stem_traits:
            if word2['2'] == word:
                print (word2['1'][0])



