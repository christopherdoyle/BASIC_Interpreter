import pytest

from basic_interpreter.basic import Token, TokenType
from basic_interpreter.interpreter import Interpreter


@pytest.mark.parametrize(
    'type_, value, representation',
    [
        (TokenType.INTEGER, 5, 'INTEGER:5'),
        (TokenType.INTEGER, None, 'INTEGER'),
    ]
)
def test_token_representation(type_, value, representation):
    assert str(Token(type_, value)) == representation


@pytest.mark.parametrize(
    'atom, atom_token',
    [
        ('5', Token(TokenType.INTEGER, 5)),
    ]
)
def test_interpreter_atomic_inputs(atom, atom_token):
    """Atomic tokens should be returned as-is."""
    assert Interpreter(atom)() == atom_token
