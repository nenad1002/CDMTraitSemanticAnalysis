import nlp_utility
from nltk.stem import WordNetLemmatizer
from nltk.stem import LancasterStemmer, SnowballStemmer
from description_analyzer import DescriptionAnalyzer
from noise_manager import NoiseManager
from trait_extractor import TraitExtractor
from trait_analyzer import TraitAnalyzer
from trait_to_attribute_matcher import TraitToAttributeMatcher
from attribute_extractor import AttributeExtractor
from attribute_name_analyzer import AttributeNameAnalyzer
from validation_runner import ValidationRunner

# Change this to false if you want to analyze a single attribute,
# otherwise specify path to the entity you want to analyze.
ANALYZE_ATTRIBUTES_FROM_SCHEMA = True

# The minimum cosine similarity when comparing attribute/traits features.
PRECISION = 0.6

# A boolean that denotes whether the program will try to find similar traits. Beware, finding similar traits
# is dependant on the vector representation of words and can be very slow.
DOES_PROCESS_SIMILAR_WORDS = False

class MainRunner:

    analyze_attributes_from_schema = True
    precision = 0
    does_process_similar_words = False

    # The trait files.
    trait_files = ['meanings.cdm.json', 'foundations.cdm.json', 'primitives.cdm.json']

    # The trait list.
    trait_list = []

    # The stemmer used by default.
    lancester = None

    # The lemmatizer used by default.
    wordnet_lemmatizer = None

    # Managers used throughout the program.
    noise_manager = None
    trait_extractor = None
    trait_analyzer = None

    # The list of stemmed trait features.
    stem_traits = []

    def __init__(self, analyze_attributes_from_schema, does_process_similar_words, precision):
        self.analyze_attributes_from_schema = analyze_attributes_from_schema
        self.precision = precision
        self.does_process_similar_words = does_process_similar_words

        # Aggresive stemming preferred.
        self.lancester = LancasterStemmer()

        # Use wordnet for lemmas.
        self.wordnet_lemmatizer = WordNetLemmatizer()

        self.noise_manager = NoiseManager()
        self.trait_extractor = TraitExtractor()
        self.trait_analyzer = TraitAnalyzer()

        # Extract traits from CDM Schema documents folder.
        self.trait_list = self.trait_extractor.extract_traits('CDM.SchemaDocuments/', self.trait_files)

        self.stem_traits = self.trait_analyzer.stem_traits(self.trait_list, self.lancester, self.wordnet_lemmatizer, self.noise_manager)


    def analyze_attributes_in_entities(self, paths, trait_to_attribute_matcher, expected_traits = None):
        '''
        Analyzes attributes in schema document entities.
        :param paths: The path to the entities.
        :param trait_to_attribute_matcher: The trait to attribute matcher.
        :param expected_traits: The expected traits to do validation.
        :return: The list of traits.
        '''
        attribute_extractor = AttributeExtractor()
        attributes = attribute_extractor.extract_attributes(paths)

        attribute_name_analyzer = AttributeNameAnalyzer()
        description_analyzer = DescriptionAnalyzer()
        attribute_to_traits_result = {}

        for attribute in attributes:
            result_traits = self.analyze_helper(attribute, attribute_name_analyzer, description_analyzer, trait_to_attribute_matcher)

            attribute_to_traits_result[attribute[0]] = set(result_traits)

        # Run the validation runner.
        if expected_traits is not None:
            validation_runner = ValidationRunner()
            example_attribute_to_trait_result = validation_runner.extract_example_data(expected_traits)
            print("The Jaccard index of similarity for the entity/entities is", validation_runner.measure_similarity(attribute_to_traits_result, example_attribute_to_trait_result))


    def analyze_single_attribute(self, attribute_name, trait_to_attribute_matcher, description):
        '''
        Analyzes a single attribute.
        :param attribute: The attribute name.
        :param trait_to_attribute_matcher: The trait to attribute matcher.
        :param description: The description.
        :return:
        '''
        attribute_name_analyzer = AttributeNameAnalyzer()
        description_analyzer = DescriptionAnalyzer()
        attribute = [attribute_name, description]

        self.analyze_helper(attribute, attribute_name_analyzer, description_analyzer, trait_to_attribute_matcher)

    def analyze_helper(self, attribute, attribute_name_analyzer, description_analyzer, trait_to_attribute_matcher):

        # Get the attribute features.
        attribute_features = attribute_name_analyzer.stem_attribute(self.lancester, self.wordnet_lemmatizer, attribute)

        # Check do we have a description, and if so process the description as defined.
        if attribute[1] != '':
            sentence_features = description_analyzer.stem_sentences(self.lancester, attribute[1], False)
        else:
            sentence_features = []

        print()
        print("------- attribute -------")
        print(attribute[0])
        print('------- traits -------')

        # We have some data.
        if (len(sentence_features) > 0):
            stemmed_sentence_features = sentence_features[0]
            unstemmed_sentence_features = sentence_features[1]
        else:
            stemmed_sentence_features = []
            unstemmed_sentence_features = []

        if len(attribute_features) > 0:
            stemmed_attribute_feature = attribute_features[0]
            unstemmed_attribute_feature = attribute_features[1]

        result_trait_set_from_attribute = trait_to_attribute_matcher.match_traits_to_attribute(
            stemmed_attribute_feature, self.stem_traits, unstemmed_attribute_feature)
        result_trait_set_from_dict = trait_to_attribute_matcher.match_traits_to_attribute(stemmed_sentence_features,
                                                                                          self.stem_traits,
                                                                                          unstemmed_sentence_features)

        result_traits = nlp_utility.define_proper_order(result_trait_set_from_attribute, result_trait_set_from_dict)
        print(result_traits)
        print('----------------')
        print()

        return result_traits

    def run(self):

        trait_to_attribute_matcher = TraitToAttributeMatcher(self.does_process_similar_words, self.precision)

        while True:
            from_schema = input("Analyze from schema (True/False)? ")
            self.analyze_attributes_from_schema = True if from_schema == 'True' else False

            if self.analyze_attributes_from_schema:
                self.analyze_attributes_in_entities(['CDM.SchemaDocuments/core/applicationCommon/Account.cdm.json'], trait_to_attribute_matcher, 'handwritten-examples/Account.trait.json')
            else:
                while (True):
                    attribute = input("Enter attribute name: ")
                    description = input("Enter description: ")

                    self.analyze_single_attribute(attribute, trait_to_attribute_matcher, description)


if __name__ == "__main__":
    main_runner = MainRunner(ANALYZE_ATTRIBUTES_FROM_SCHEMA, DOES_PROCESS_SIMILAR_WORDS, PRECISION)
    main_runner.run()
