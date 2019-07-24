# This file will implement functions which will deal with noise.

noise_features = ['type']

def is_generating_too_much_noise(feature):
    if feature in noise_features:
        return True

    return False

def find_commonly_occured_noise(traits):
    # TODO: Find a way to remove trait features that might only appear once.
    trait_features_count = {}
    for trait in traits:
        #print (trait)
        for i in range(len(trait[1]) - 1, -1, -1):
            if i == len(trait[1]) - 1:
                continue
            if trait_features_count.get(trait[1][i]) is None:
                trait_features_count[trait[1][i]] = 1
            else:
                trait_features_count[trait[1][i]] += 1

    for trait_feature in sorted(trait_features_count, key=trait_features_count.get, reverse=True):
        if trait_features_count[trait_feature] >= 2:
            noise_features.append(trait_feature)