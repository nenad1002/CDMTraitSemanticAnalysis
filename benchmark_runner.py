import json

def extract_example_data(file):
    example_dict = {}

    with open(file) as json_file:
        data = json.load(json_file)
        for trait in data["data"]:
            attribute_name = trait.get('attribute')
            trait_set = set(trait.get('traits'))
            example_dict[attribute_name] = trait_set

    return example_dict

# Measures Jaccard index to measure the similarity between actual and expected set.
def measure_similarity(original_set, example_set):
    diff1 = 0
    diff2 = 0
    total1 = 0
    total2 = 0

    for output_att in original_set:
        if output_att in example_set:
            original_set_item = original_set[output_att]
            example_set_item = example_set[output_att]
            diff1 += len(original_set_item.intersection(example_set_item))
            diff2 += len(example_set_item.difference(original_set_item))
            total1 += len(original_set_item)
            total2 += len(example_set_item)

    intersect = diff1
    union = total1 + total2 - intersect
    jaccard_index = intersect / union

    return jaccard_index
