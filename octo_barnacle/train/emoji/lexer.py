import enum
import string
import io
import collections

VALID_CODE_POINT_LETTER = string.digits + 'ABCDEF'


class PeekableStringIO(io.StringIO):

    def peek(self, size=-1):
        current_offset = self.tell()
        try:
            return self.read(size)
        finally:
            self.seek(current_offset)


class TokenType(enum.Enum):
    CodePoint = enum.auto()
    Status = enum.auto()
    Comment = enum.auto()


Token = collections.namedtuple('Token', 'type value')


def tokenize(text):
    buf = PeekableStringIO(text)
    peek_chr = buf.peek(1)
    while peek_chr:
        if peek_chr in string.whitespace:
            buf.read(1)
            pass
        elif peek_chr == '#':
            buf.read(1)
            yield _tokenize_comment(buf)
        elif peek_chr == ';':
            buf.read(1)
            yield _tokenize_status(buf)
        elif peek_chr in VALID_CODE_POINT_LETTER:
            yield _tokenize_code_point(buf)
        else:
            raise InvalidCharacterError(peek_chr)
        peek_chr = buf.peek(1)


def _tokenize_comment(buf):
    result = io.StringIO()
    peek_chr = buf.peek(1)
    while peek_chr and peek_chr != '\n':
        result.write(buf.read(1))
        peek_chr = buf.peek(1)
    return Token(TokenType.Comment, result.getvalue().strip())


def _tokenize_status(buf):
    result = io.StringIO()
    peek_chr = buf.peek(1)
    while peek_chr and peek_chr not in ('\n', '#'):
        result.write(buf.read(1))
        peek_chr = buf.peek(1)
    return Token(TokenType.Status, result.getvalue().strip())


def _tokenize_code_point(buf):
    result = io.StringIO()
    peek_chr = buf.peek(1)
    while peek_chr in VALID_CODE_POINT_LETTER:
        result.write(buf.read(1))
        peek_chr = buf.peek(1)
    return Token(TokenType.CodePoint, result.getvalue())


class InvalidCharacterError(Exception):

    def __init__(self, character):
        self.character = character

    def __str__(self):
        return "{}:{}".format(ord(self.character), self.character)