import abc
import inspect
from typing import Type


class TokenType(metaclass=abc.ABCMeta):

    name = None
    parsers = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not inspect.isabstract(cls):
            # i.e. if not an abstract class
            cls.parsers.append(cls.parse)

    @staticmethod
    def _eat_pre_whitespace(text: str):
        stripped = text.lstrip()
        return stripped, len(text) - len(stripped)

    @classmethod
    @abc.abstractmethod
    def parse(cls, value: str) -> (Type, int):
        """Tries to parse given input string LTR as Type class represents,
        returning (None, 0) if it cannot be parsed, else returning the parsed
        portion of the input as the correct type, and the position of the next
        character in the input string.
        """
        pass


class ValueTokenType(TokenType, metaclass=abc.ABCMeta):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

    @classmethod
    @abc.abstractmethod
    def add(cls, left, right) -> "Token":
        pass

    @classmethod
    @abc.abstractmethod
    def sub(cls, left, right) -> "Token":
        pass

    @classmethod
    @abc.abstractmethod
    def mul(cls, left, right) -> "Token":
        pass

    @classmethod
    @abc.abstractmethod
    def div(cls, left, right) -> "Token":
        pass


class OperatorTokenType(TokenType, metaclass=abc.ABCMeta):
    @classmethod
    @abc.abstractmethod
    def __call__(cls, left: "Token", right: "Token") -> "Token":
        pass

    @property
    @abc.abstractmethod
    def symbol(self):
        pass

    @classmethod
    def parse(cls, value: str):
        _, pos = cls._eat_pre_whitespace(value)
        if value[pos] == cls.symbol:
            return None, pos + 1
        else:
            return None, 0


class Token:
    def __init__(self, type_: Type[TokenType], value=None):
        self.type_ = type_
        self.value = value

    def __call__(self, *args, **kwargs):
        return self.type_.__call__(*args, **kwargs)

    def __str__(self):
        if self.value is None:
            return self.type_.name
        else:
            return f"{self.type_.name}:{self.value}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other: "Token"):
        return self.type_ == other.type_ and self.value == other.value

    def __add__(self, other: "Token"):
        assert self.type_ is other.type_
        return self.type_.add(self.value, other.value)

    def __sub__(self, other: "Token"):
        assert self.type_ is other.type_
        return self.type_.sub(self.value, other.value)

    def __mul__(self, other: "Token"):
        assert self.type_ is other.type_
        return self.type_.mul(self.value, other.value)

    def __truediv__(self, other: "Token"):
        assert self.type_ is other.type_
        return self.type_.div(self.value, other.value)


class INTEGER(ValueTokenType):

    name = "INTEGER"

    @classmethod
    def add(cls, left: int, right: int) -> Token:
        return Token(cls, left + right)

    @classmethod
    def sub(cls, left: int, right: int) -> Token:
        return Token(cls, left - right)

    @classmethod
    def parse(cls, value: str):
        _, starting_pos = cls._eat_pre_whitespace(value)
        pos = starting_pos
        while pos < len(value) and value[pos].isdigit():
            pos += 1

        if pos == starting_pos:
            return None, pos
        else:
            return int(value[starting_pos:pos]), pos

    @classmethod
    def mul(cls, left, right) -> "Token":
        return Token(cls, left * right)

    @classmethod
    def div(cls, left, right) -> "Token":
        return Token(cls, int(left / right))


class PLUS(OperatorTokenType):

    name = "PLUS"
    symbol = "+"

    @classmethod
    def __call__(cls, left: Token, right: Token):
        return left + right


class MINUS(OperatorTokenType):

    name = "MINUS"
    symbol = "-"

    @classmethod
    def __call__(cls, left: Token, right: Token):
        return left - right


class MULT(OperatorTokenType):

    name = "MULT"
    symbol = "*"

    @classmethod
    def __call__(cls, left: Token, right: Token):
        return left * right


class DIV(OperatorTokenType):

    name = "DIV"
    symbol = "/"

    @classmethod
    def __call__(cls, left: Token, right: Token):
        return left / right


def parse(text: str) -> (Token, int):
    """Parses text to a token and an end-position, by the principle that the
    best match is the parser which can gobble the _most_ text from the input
    string.
    """
    # parser, parser_value, parser_position
    scores = [(parser, *parser(text)) for parser in TokenType.parsers]
    # sort by position descending
    scores.sort(key=lambda x: -x[2])
    if scores[0][2] == 0:
        # everything failed to parse
        raise TypeError
    else:
        return Token(scores[0][0].__self__, scores[0][1]), scores[0][2]
