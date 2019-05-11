import re

PATTERN_EMOJI = re.compile(r'[\U0001f600-\U0001f64f]')
PATTERN_SYMBOL = re.compile(r'[\U0001f300-\U0001f5ff]')


def is_emoji(text):
    return bool(PATTERN_EMOJI.match(text))


def is_symbol(text):
    return bool(PATTERN_SYMBOL.match(text))
