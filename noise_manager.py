class NoiseManager:
    '''Noise manager is a class which deals with noise among features and it tries to throw away traits
    which might be too noisy for additional processing. This means that all traits are still candidates
    for classification process, but the noisy traits will never be included if our features only match trait's
    noisy features (which are usually all of them but last one since the last featue is usually most descriptive)

    e.g.
    means.demographic.age trait, the last feature "age" is the most descriptive, but means and demographic will
    usually be the noisy features and won't always be matched.
    '''


    # Add noise features which we want to usually exclude no matter what.
    noise_features = ['type']

    def is_generating_too_much_noise(self, feature):
        if feature in self.noise_features:
            return True

            return False


    def generate_commonly_occured_noise(self, traits):
        '''
        Finds and generates trait features which might be
        too noisy and not really useful for classification.
        :param traits: The list of existing traits.
        :return: The noisy traits.
        '''

        # TODO: Find a way to remove trait features that might only appear once.
        trait_features_count = {}
        for trait in traits:
            for i in range(len(trait[1]) - 1, -1, -1):
                # Last feature of a trait can never be exluded since it is almost always useful.
                if i == len(trait[1]) - 1:
                    continue

                # Update map with the specific count
                if trait_features_count.get(trait[1][i]) is None:
                    trait_features_count[trait[1][i]] = 1
                else:
                    trait_features_count[trait[1][i]] += 1

        for trait_feature in sorted(trait_features_count, key=trait_features_count.get, reverse=True):

            # Only features which appear more than once in different traits are included since if only one trait has
            # some feature, we can safely assume that feature is not noisy (although it might be in some cases).
            if trait_features_count[trait_feature] >= 2:
                self.noise_features.append(trait_feature)