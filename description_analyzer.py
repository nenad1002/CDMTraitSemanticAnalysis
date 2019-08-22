import nlp_utility
import spacy


class DescriptionAnalyzer:
    '''
    The class that deals with analyzing an attribute's descrption.
    '''

    nlp = None


    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")


    def stem_sentences(self, stemmer, sent, is_noise_preferred):

        # Create a spacy doc.
        doc = self.nlp(sent)

        # We are generating both stemmed and non-stemmed words at this point.
        subjects = self.find_text_roots_subjects_or_objects(doc)
        stemmed_subjects = self.stem_all_words(subjects, stemmer)

        # Find the named entities inside the description.
        named_entities = self.find_named_entity_nouns(doc)
        stemmed_entities = self.stem_all_words(named_entities, stemmer)

        stemmed_result = list(set(stemmed_subjects).union(set(stemmed_entities)))
        non_stemmed_result = list(set(subjects).union(set(named_entities)))

        # If we can accept more noise, then we can go through all of the nouns.
        if is_noise_preferred:
            all_nouns = self.find_all_nouns(doc)
            stemmed_all_nouns = self.stem_all_words(all_nouns, stemmer)
            stemmed_result = list(set(stemmed_result).union(stemmed_all_nouns))
            non_stemmed_result = list(set(non_stemmed_result).union(all_nouns))

        return stemmed_result, non_stemmed_result


    def find_text_roots_subjects_or_objects(self, doc):
        '''
        Find the text root, subjects or objects.
        :param doc: The NLP tokenized doc.
        :return: The list of words.
        '''

        subjects = []
        objects = []

        for chunk in doc.noun_chunks:

            # Finding nominal subjects/root or objects.
            if chunk.root.dep_ == 'nsubj' or chunk.root.dep_ == 'dobj' or chunk.root.dep_ == 'ROOT' or chunk.root.dep_ == 'conj':

                # Uncomment this if we want to import custom stop words into our code.
                # TODO: Create an injector for custom stop words into our code through configs.
                # tokens = nlp_utility.remove_stop_words(chunk.text.split())

                for token in self.nlp(chunk.text):
                    # Check if the current root word is a subject, root or conjunction connecting at least one subject or ROOT.
                    if chunk.root.dep_ == 'nsubj' or chunk.root.dep_ == 'ROOT' or (chunk.root.dep_ == 'conj' and (chunk.root.head.dep_ == 'nsubj' or chunk.root.head.dep_ == 'ROOT')):
                        if not token.is_stop:
                            subjects.append(token.text.lower())
                    elif chunk.root.dep_ == 'dobj' or (chunk.root.dep_ == 'conj' and chunk.root.head.dep_ == 'dobj'):
                        if not token.is_stop:
                            objects.append(token.text.lower())

        # If the sentence doesn't have any subjects or roots (very unlikely) find all nouns because all of them might be important.
        if len(subjects) == 0 and len(objects) == 0:
            return self.find_all_nouns(doc)

        print (subjects)
        print (objects)
        return subjects if len(subjects) != 0 else objects


    # TODO: Change this function to properly reflect named entities.
    def find_named_entity_nouns(self, doc):
        '''
        Find named entity nouns.

        e.g. the text "8/21/2019" would return the "DATE" entity label
        :param doc: The tokenized doc.
        :return: The entity noun keyword which can easily be connected with the appropriate trait.
        '''
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

    def find_all_nouns(self, doc):
        '''
        Find all nouns in the doc.
        :param doc: The tokenized doc.
        :return: The list of nouns.
        '''

        result = []
        for chunk in doc.noun_chunks:
            tokens = nlp_utility.remove_stop_words([chunk.root.text])
            for token in tokens:
                result.append(token.lower())

        return result


    def stem_all_words(self, word_list, stemmer):
        result = []
        for word in word_list:
            result.append(stemmer.stem(word))
        return result