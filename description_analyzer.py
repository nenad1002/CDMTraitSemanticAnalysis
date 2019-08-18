from nltk.tokenize import word_tokenize
from nltk import pos_tag
import nlp_utility
import spacy

nlp = spacy.load("en_core_web_lg")

# Deprecated, use Spacy method instead for both increased precision and speed.
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

def lemma_and_stem_sentence_spacy(stemmer, sent, is_noise_preferred):
    text = (sent)

    # Create a spacy doc
    doc = nlp(text)

    # If we don't want much noise we will need to ignore some nouns and all other words.
    if is_noise_preferred == False:
        return find_text_subjects(doc, stemmer)
    else:
        subjects = find_text_subjects(doc, stemmer)
        named_entities = find_named_entity_nounts(doc, stemmer)
        all_founds = find_all_nouns(doc, stemmer)

        return list(set(subjects).union(set(named_entities).union(set(all_founds))))

    #result = []
    #for noun_chunk in doc.noun_chunks:
    #    print ("noun chunk" + noun_chunk.text.lower())
    #    stem = stemmer.stem(noun_chunk.text.lower())
    #    result.append(stem)

    #   return result

def find_text_subjects(doc, stemmer):
    subjects = []
    objects = []
    for chunk in doc.noun_chunks:
        # Finding nominal subjects.
        if chunk.root.dep_ == 'nsubj' or chunk.root.dep_ == 'dobj':

            # Add lemma of a name to the list
            tokens = nlp_utility.remove_stop_words(chunk.text.split())
            for token in tokens:
                if chunk.root.dep_ == 'nsubj':
                    subjects.append(stemmer.stem(token.lower()))
                else:
                    objects.append(stemmer.stem(token.lower()))

    print (subjects)
    print (objects)
    return subjects if len(subjects) != 0 else objects


def find_named_entity_nounts(doc, stemmer):
    nouns = find_named_entity_nouns_processor(doc)
    res = []
    for noun in nouns:
        res.append(stemmer.stem(noun))

    return res


# TODO: Change this function to properly reflect named entities.
def find_named_entity_nouns_processor(doc):
    for ent in doc.ents:
        if ent.label_ == 'ORG':
            return ['organization', 'company']
        if ent.label_ == 'MONEY':
            return ['currency']
        if ent.label_ == 'GPE':
            return ['address']
        if ent.label_ == 'DATE':
            return ['date']
        if ent.label_ == 'TIME':
            return ['time']

    return []

def find_all_nouns(doc, stemmer):
    result = []
    for chunk in doc.noun_chunks:
        tokens = nlp_utility.remove_stop_words([chunk.root.text])
        for token in tokens:
            result.append(stemmer.stem(token.lower()))

    return result
