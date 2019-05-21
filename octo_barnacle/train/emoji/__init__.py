"""package for downloading and parsing data from full emoji list

this package is designed for parsing emoji-test.txt
see: https://unicode.org/Public/emoji/12.0/emoji-test.txt
"""
import requests
from .lexer import tokenize
from .parser import parse_emojis

EMOJI_TEST_URL = 'https://unicode.org/Public/emoji/12.0/emoji-test.txt'


def get_emoji_codepoints():
    """get all emoji code points 

    this method does:
        - download emoji-test.txt
        - parse and return all emoji code points

    Returns:
        list of string that represent emoji
    """
    res = requests.get(EMOJI_TEST_URL)
    tokens = tokenize(res.text)
    emojis = parse_emojis(tokens)
    return [emoji.codepoints for emoji in emojis]
