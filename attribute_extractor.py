import json


class AttributeExtractor:
    '''
    Extracts attributes only from non-resolved schema files, could be changed to look into resolved files.
    '''

    def extract_attributes(self, files_to_open):
        '''
        Extracts attributes
        :param files_to_open: The list of files to extract the attributes from.
        :return: The list of attribute/description pairs.
        '''

        attributes = []

        for file in files_to_open:
            with open(file) as json_file:
                data = json.load(json_file)
                for attribute in data['definitions'][0]['hasAttributes'][0]['attributeGroupReference']['members']:
                    if 'name' in attribute:
                        attribute_name = attribute.get('name')
                        description = ''

                        # Check if it has a description.
                        if 'appliedTraits' in attribute:
                            for trait in attribute['appliedTraits']:
                                if 'traitReference' in trait:
                                    trait_name = trait.get('traitReference')
                                    if trait_name == 'is.localized.describedAs':
                                        description = trait['arguments'][0]['entityReference']['constantValues'][0][1]

                        attributes.append((attribute_name, description))

        return attributes

