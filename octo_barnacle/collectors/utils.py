import string


_trans_remove_punctuation = str.maketrans('', '', string.punctuation)
_trans_remove_whitespace = str.maketrans('', '', string.whitespace)


def gen_remove_punctuation(str_gen):
    """remove punctuation of string from given generator

    Arguments:
        str_gen: expect string iterable

    Return:
        generator that generate string
    """
    return (s.translate(_trans_remove_punctuation) for s in str_gen)


def gen_remove_whitespace(str_gen):
    """remove whitespace of string from given generator

    Arguments:
        str_gen: expect string iterable

    Return:
        generator that generate string
    """
    return (s.translate(_trans_remove_whitespace) for s in str_gen)
