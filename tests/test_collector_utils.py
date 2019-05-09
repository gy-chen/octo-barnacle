from octo_barnacle.collectors import utils


def test_remove_punctation():
    result = list(utils.gen_remove_punctuation(
        ['!aaaa!', 'bb,bb', '.c.c.c.c']))

    assert result == ['aaaa', 'bbbb', 'cccc']


def test_remove_whitespace():
    result = list(utils.gen_remove_whitespace(
        [' aaaa ', 'bb bb', ' c c c c']))

    assert result == ['aaaa', 'bbbb', 'cccc']
