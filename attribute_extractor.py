# Extracts attributes only from non-resolved schema files, could be changed to look into resolved files.

import json

def extract_attributes(files_to_open):
    attributes = []

    for file in files_to_open:
        with open(file) as json_file:
            data = json.load(json_file)
            for attribute in data['definitions'][0]['hasAttributes'][0]['attributeGroupReference']['members']:
                if 'name' in attribute:
                    attribute_name = attribute.get('name')
                    description = ''
                    if 'appliedTraits' in attribute:
                        for trait in attribute['appliedTraits']:
                            if 'traitReference' in trait:
                                trait_name = trait.get('traitReference')
                                if trait_name == 'is.localized.describedAs':
                                    description = trait['arguments'][0]['entityReference']['constantValues'][0][1]

                    attributes.append((attribute_name, description))

    return attributes

