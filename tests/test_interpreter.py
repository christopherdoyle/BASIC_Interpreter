import pytest

from basic_interpreter.basic import Token, INTEGER, PLUS
from basic_interpreter.interpreter import Interpreter, Lexer


class DummyLexer:

    def __init__(self, tokens):
        self.tokens = tokens

    def parse_tokens_iter(self):
        yield from self.tokens


def int_add_lexer_factory(integers):
    lexer = Lexer('')

    integer_iter = iter(integers[:-1])

    def _iter(*args, **kwargs):
        while True:
            try:
                yield Token(INTEGER, next(integer_iter))
                yield Token(PLUS, '+')
            except StopIteration:
                break
        yield Token(INTEGER, integers[-1])

    lexer.parse_tokens_iter = _iter
    return lexer


@pytest.mark.parametrize(
    'atom, atom_token',
    [
        ('5', [Token(INTEGER, 5)]),
        ('125', [Token(INTEGER, 125)]),
        ('+', [Token(PLUS, '+')]),
        ('++', [Token(PLUS, '+'), Token(PLUS, '+')]),
        ('3+5', [Token(INTEGER, 3), Token(PLUS, '+'), Token(INTEGER, 5)]),
        ('3 + 5', [Token(INTEGER, 3), Token(PLUS, '+'), Token(INTEGER, 5)]),
    ]
)
def test_lexer_parse_tokens(atom, atom_token):
    assert Lexer(atom).parse_tokens() == atom_token


@pytest.mark.parametrize(
    'text', ['5 + +', '2 2', '+', '+ 1 2', '9 3 +']
)
def test_lexer_evaluates_bad_grammar_type_error(text):
    with pytest.raises(TypeError):
        Lexer(text).parse_tokens()


@pytest.mark.parametrize(
    'lexed_text, result',
    [
        (int_add_lexer_factory([2, 5]), Token(INTEGER, 7)),
        (int_add_lexer_factory([1, 2, 3, 4]), Token(INTEGER, 10)),
    ]
)
def test_interpreter_evaluates_integer_addition(lexed_text, result):
    assert Interpreter(lexed_text)() == result
