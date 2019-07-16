# This file will implement functions which will deal with noise.

def is_generating_too_much_noise(feature):
    if feature == 'identity' or feature == 'date':
        return True

    return False;