from nltk.tokenize import word_tokenize
from nltk import pos_tag
import nlp_utility


def lemma_and_stem_sentence(stemmer, sent):
    sentence_words = word_tokenize(sent)
    pos = pos_tag(sentence_words)
    sentence_words = nlp_utility.remove_stop_words(sentence_words)

    result = []
    for word in pos:
        # Find nouns.
        if word[1] == 'NN' or word[1] == 'NNS' or word[1] == 'NNP':
            stem = stemmer.stem(word[0].lower())
            result.append(stem)

    return result
