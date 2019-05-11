import string
from octo_barnacle.bot import utils


def test_is_emoji():
    for o in range(ord('\U0001f600'), ord('\U0001f64f')+1):
        assert utils.is_emoji(chr(o))


def test_is_not_emoji():
    for s in string.printable:
        assert not utils.is_emoji(s)


def test_is_symbol():
    for o in range(ord('\U0001f300'), ord('\U0001f5ff')+1):
        assert utils.is_symbol(chr(o))


def test_is_not_symbol():
    for s in string.printable:
        assert not utils.is_symbol(s)
