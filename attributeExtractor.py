# Extracts attributes only from non-resolved schema files, could be changed to look into resolved files.

import json

def extract_attributes(files_to_open):
    attributes = []

    for file in files_to_open:
        with open(file) as json_file:
            data = json.load(json_file)
            print (data)
            for attribute in data['definitions'][0]['hasAttributes'][0]['attributeGroupReference']['members']:
                if 'name' in attribute:
                    attribute_name = attribute.get('name')
                    attributes.append(attribute_name)

    return attributes

