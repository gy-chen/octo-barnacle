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


def gen_append_range_number(str_gen, from_, to):
    """append number to string from given generator

    beside generate string that appended number, it also generate original string.

    e.g. gen_append_range_number('aaa', 1, 1) -> ('aaa', 'aaa1')

    Arguments:
        str_gen: expect string iterable
        from_: start of appendix number range 
        to: end of appendix number range (include)

    Return:
        generator that generate string
    """
    for s in str_gen:
        yield s
        for num in range(from_, to+1):
            yield '{}{}'.format(s, num)
