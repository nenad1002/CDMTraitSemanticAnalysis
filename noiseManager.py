# This file will implement functions which will deal with noise.

def is_generating_too_much_noise(feature):
    if feature == 'identity' or feature == 'date' or feature == 'currency' or feature == 'type':
        return True

    return False;