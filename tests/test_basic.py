import pytest

from basic_interpreter.basic import Token


@pytest.mark.parameterized(
    'type_, value, representation',
    []
)
def test_token_representation(type_, value, representation):
    assert str(Token(type_, value)) == representation

