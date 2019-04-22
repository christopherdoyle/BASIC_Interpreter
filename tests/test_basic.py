from functools import reduce

import pytest

from basic_interpreter import basic
from basic_interpreter.basic import Token, INTEGER, parse


@pytest.mark.parametrize(
    "token, other, equal",
    [
        (Token(INTEGER, 3), Token(INTEGER, 3), True),
        (Token(INTEGER, 3), Token(INTEGER, 6), False),
        (Token(INTEGER, 3), Token(INTEGER, 3.5), False),
    ],
)
def test_token_equality(token: Token, other: Token, equal: bool):
    assert (token == other) == equal


@pytest.mark.parametrize("type_, value, representation", [(INTEGER, 5, "INTEGER:5"), (INTEGER, None, "INTEGER")])
def test_token_representation(type_, value, representation):
    assert str(Token(type_, value)) == representation


@pytest.mark.parametrize("symbol", ["5", "+", "102", "-", "*"])
def test_try_cast_successful(symbol):
    parse(symbol)


@pytest.mark.parametrize("left, right, output", [(1, 4, 5), (-5, 120, 115), (0, 0, 0)])
def test_token_integer_addition(left, right, output):
    assert basic.PLUS()(Token(INTEGER, left), Token(INTEGER, right)) == Token(INTEGER, output)


@pytest.mark.parametrize("left, right, output", [(1, 4, -3), (-5, 8, -13), (4, 0, 4)])
def test_token_integer_minus(left, right, output):
    assert basic.MINUS()(Token(INTEGER, left), Token(INTEGER, right)) == Token(INTEGER, output)


@pytest.mark.parametrize("left, right, output", [(1, 4, 4), (-5, 8, -40), (4, 0, 0), (0, 0, 0)])
def test_token_integer_mult(left, right, output):
    assert basic.MULT()(Token(INTEGER, left), Token(INTEGER, right)) == Token(INTEGER, output)


@pytest.mark.parametrize("left, right, output", [(1, 4, 0), (10, 2, 5), (7, 2, 3), (7, 3, 2)])
def test_token_integer_division(left, right, output):
    assert basic.DIV()(Token(INTEGER, left), Token(INTEGER, right)) == Token(INTEGER, output)
