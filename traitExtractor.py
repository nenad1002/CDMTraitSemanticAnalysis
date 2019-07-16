import json

def is_feature_valuable(feature):
    # TODO
    return True

def extract_trait_words(trait_name):
    trait_words = []
    for trait_feature in trait_name.split('.'):
        if is_feature_valuable(trait_feature):
            trait_words.append(trait_feature)

    return trait_words


def extract_traits(folder, files_to_open):
    trait_name_list = []

    for file in files_to_open:
        with open(folder + file) as json_file:
            data = json.load(json_file)
            for trait in data['definitions']:
                if 'traitName' in trait:
                    trait_name = trait.get('traitName')
                    trait_words = extract_trait_words(trait_name)
                    trait_tuple = trait_name, trait_words
                    trait_name_list.append(trait_tuple)

    return trait_name_list