import json

class TraitExtractor:
    '''
    The class the reads traits from the schema documents.
    '''

    def extract_trait_features(self, trait_name):
        trait_words = []
        for trait_feature in trait_name.split('.'):
            trait_words.append(trait_feature)

        return trait_words


    def extract_traits(self, folder, files_to_open):
        trait_name_list = []

        for file in files_to_open:
            with open(folder + file) as json_file:
                data = json.load(json_file)
                for trait in data['definitions']:
                    if 'traitName' in trait:
                        trait_name = trait.get('traitName')
                        trait_features = self.extract_trait_features(trait_name)
                        trait_tuple = trait_name, trait_features
                        trait_name_list.append(trait_tuple)

        return trait_name_list