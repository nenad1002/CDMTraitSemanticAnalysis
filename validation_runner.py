import json

class ValidationRunner:
    '''
    The class the validates the final results by providing some metrics.
    '''


    def extract_example_data(self, file):
        '''
        Extracts a sample user-defined attribute/description-the result trait data.
        :return: A dictionary of attribute name and trait set key.
        '''

        example_dict = {}

        with open(file) as json_file:
            data = json.load(json_file)
            for trait in data["data"]:
                attribute_name = trait.get('attribute')
                trait_set = set(trait.get('traits'))
                example_dict[attribute_name] = trait_set

        return example_dict


    def measure_similarity(self, original_set, example_set):
        '''
        Measures Jaccard index to measure the similarity between the actual and expected set.
        :param original_set: The original set, returned as a result.
        :param example_set: The example set.
        :return: A floating number, denoting the similarity between 0 and 1.
        '''
        diff1 = 0
        diff2 = 0
        total1 = 0
        total2 = 0

        for output_att in original_set:
            if output_att in example_set:
                original_set_item = original_set[output_att]
                example_set_item = example_set[output_att]

                # Calculate intersection and difference between two sets.
                diff1 += len(original_set_item.intersection(example_set_item))
                diff2 += len(example_set_item.difference(original_set_item))
                total1 += len(original_set_item)
                total2 += len(example_set_item)

        intersect = diff1
        union = total1 + total2 - intersect
        jaccard_index = intersect / union

        return jaccard_index
