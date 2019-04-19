import pytest

from basic_interpreter.basic import Token, TokenType


@pytest.mark.parametrize(
    'type_, value, representation',
    [
        (TokenType.INTEGER, 5, 'INTEGER:5'),
        (TokenType.INTEGER, None, 'INTEGER'),
    ]
)
def test_token_representation(type_, value, representation):
    assert str(Token(type_, value)) == representation
