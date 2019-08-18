from nltk.tokenize import word_tokenize
from nltk import pos_tag
import nlp_utility
import spacy

nlp = spacy.load("en_core_web_md")

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

    # We are generating both stemmed and unstemmed words at this point.
    stemmed_result = []
    non_stemmed_result = []

    subjects = find_text_subjects(doc)
    stemmed_subjects = stem_all_words(subjects, stemmer)

    named_entities = find_named_entity_nouns(doc)
    stemmed_entities = stem_all_words(named_entities, stemmer)

    stemmed_result = list(set(stemmed_subjects).union(set(stemmed_entities)))
    non_stemmed_result = list(set(subjects).union(set(named_entities)))

    # If we can accept more noise we can go through all of the nouns.
    if is_noise_preferred:
        all_nouns = find_all_nouns(doc)
        stemmed_all_nouns = stem_all_words(all_nouns, stemmer)
        stemmed_result = list(set(stemmed_result).union(non_stemmed_result))
        non_stemmed_result = list(set(non_stemmed_result).union(all_nouns))

    return stemmed_result, non_stemmed_result

def find_text_subjects(doc):
    subjects = []
    objects = []
    for chunk in doc.noun_chunks:
        # Finding nominal subjects/root or objects.
        if chunk.root.dep_ == 'nsubj' or chunk.root.dep_ == 'dobj' or chunk.root.dep_ == 'ROOT' or chunk.root.dep_ == 'conj':

            # Add lemma of a name to the list
            tokens = nlp_utility.remove_stop_words(chunk.text.split())
            for token in tokens:
                if chunk.root.dep_ == 'nsubj' or chunk.root.dep_ == 'ROOT' or (chunk.root.dep_ == 'conj' and chunk.root.head.dep_ == 'nsubj'):
                    subjects.append(token.lower())
                elif chunk.root.dep_ == 'dobj' or (chunk.root.dep_ == 'conj' and chunk.root.head.dep_ == 'dobj'):
                    objects.append(token.lower())

                #if chunk.root.dep_ == 'conj':
                #    if find_conj_subject(subjects, chunk.root.head.text)

    print (subjects)
    print (objects)

    # If a sentence doesn't have any subjects or root (very unlikely) find all nouns because all of them might be important.
    if len(subjects) == 0 and len(objects) == 0:
        return find_all_nouns(doc)

    return subjects if len(subjects) != 0 else objects


# TODO: Change this function to properly reflect named entities.
def find_named_entity_nouns(doc):
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

def find_all_nouns(doc):
    result = []
    for chunk in doc.noun_chunks:
        tokens = nlp_utility.remove_stop_words([chunk.root.text])
        for token in tokens:
            result.append(token.lower())

    return result

def stem_all_words(word_list, stemmer):
    result = []
    for word in word_list:
        result.append(stemmer.stem(word))
    return result