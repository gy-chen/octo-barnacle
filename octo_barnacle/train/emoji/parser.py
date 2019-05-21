import collections
import itertools
from .lexer import TokenType


class PeekableIterator:

    def __init__(self, iterator):
        self._iterator = iterator

    def peek(self):
        try:
            item = next(self._iterator)
            self._iterator = itertools.chain([item], self._iterator)
            return item
        except StopIteration:
            return None

    def __iter__(self):
        return self._iterator

    def __next__(self):
        return self._iterator.__next__()


Emoji = collections.namedtuple('Emoji', 'codepoints status comment')


def parse_emojis(tokens):
    tokens = PeekableIterator(tokens)
    peek_token = tokens.peek()
    while peek_token:
        if peek_token.type == TokenType.Comment:
            next(tokens)
            pass
        elif peek_token.type == TokenType.CodePoint:
            yield _parse_emoji(tokens)
        else:
            raise UnexpectTokenError(peek_token)
        peek_token = tokens.peek()


def _parse_emoji(tokens):
    codepoints = ''
    status = None
    comment = None

    token = next(tokens)
    while token.type == TokenType.CodePoint:
        codepoints += chr(int(token.value, 16))
        token = next(tokens)

    if token.type != TokenType.Status:
        raise UnexpectTokenError(token)
    status = token.value

    token = next(tokens)
    if token.type != TokenType.Comment:
        raise UnexpectTokenError(token)
    comment = token.value

    return Emoji(codepoints, status, comment)


class UnexpectTokenError(Exception):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return str(self.token)
