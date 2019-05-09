from octo_barnacle.collectors import utils


def test_remove_punctation():
    result = list(utils.gen_remove_punctuation(
        ['!aaaa!', 'bb,bb', '.c.c.c.c']))

    assert result == ['aaaa', 'bbbb', 'cccc']


def test_remove_whitespace():
    result = list(utils.gen_remove_whitespace(
        [' aaaa ', 'bb bb', ' c c c c']))

    assert result == ['aaaa', 'bbbb', 'cccc']


def test_append_range_number():
    result = list(utils.gen_append_range_number(
        ['aaa', 'bbb'],
        1, 3
    ))

    assert result == ['aaa', 'aaa1', 'aaa2',
                      'aaa3', 'bbb', 'bbb1', 'bbb2', 'bbb3']
