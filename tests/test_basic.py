import pytest

from basic_interpreter.basic import Token, INTEGER, PLUS, parse
from basic_interpreter.interpreter import Interpreter


@pytest.mark.parametrize(
    'token, other, equal',
    [
        (Token(INTEGER, 3), Token(INTEGER, 3), True),
        (Token(INTEGER, 3), Token(INTEGER, 6), False),
        (Token(INTEGER, 3), Token(INTEGER, 3.5), False),
    ]
)
def test_token_equality(token: Token, other: Token, equal: bool):
    assert (token == other) == equal


@pytest.mark.parametrize(
    'type_, value, representation',
    [
        (INTEGER, 5, 'INTEGER:5'),
        (INTEGER, None, 'INTEGER'),
    ]
)
def test_token_representation(type_, value, representation):
    assert str(Token(type_, value)) == representation


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
def test_interpreter_parse_tokens(atom, atom_token):
    assert Interpreter(atom).parse_tokens() == atom_token


@pytest.mark.parametrize(
    'symbol',
    ['5', '+', '102']
)
def test_try_cast_successful(symbol):
    parse(symbol)


@pytest.mark.parametrize(
    'text, result',
    [
        ('5 + 2', Token(INTEGER, 7)),
        ('1 + 2 + 3 + 4', Token(INTEGER, 10)),
    ]
)
def test_interpreter_evaluates_integer_addition(text, result):
    assert Interpreter(text)() == result
