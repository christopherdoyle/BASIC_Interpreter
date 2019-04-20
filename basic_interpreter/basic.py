from typing import Type


class TokenType:

    name = None
    parsers = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.parsers.append(cls.parse)

    @staticmethod
    def _eat_pre_whitespace(text: str):
        stripped = text.lstrip()
        return stripped, len(text) - len(stripped)

    @staticmethod
    def add(left, right):
        raise NotImplementedError

    @classmethod
    def parse(cls, value) -> (Type, int):
        raise NotImplementedError


class Token:

    def __init__(self, type_: Type[TokenType], value):
        self.type_ = type_
        self.value = value

    def __str__(self):
        if self.value is None:
            return self.type_.name
        else:
            return f'{self.type_.name}:{self.value}'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other: 'Token'):
        return self.type_ == other.type_ and self.value == other.value

    def __add__(self, other: 'Token'):
        assert self.type_ is other.type_
        self.type_.add(self.value, other.value)


class INTEGER(TokenType):

    name = 'INTEGER'

    @classmethod
    def add(cls, left: int, right: int) -> int:
        return left + right

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


class OPERATOR:

    @classmethod
    def __call__(cls, left, right):
        raise NotImplementedError


class PLUS(TokenType, OPERATOR):

    name = '+'

    @classmethod
    def __call__(cls, left: Token, right: Token):
        return left + right

    @classmethod
    def parse(cls, value: str):
        _, pos = cls._eat_pre_whitespace(value)
        if value[pos] == '+':
            return '+', pos + 1
        else:
            return None, 0


def parse(text: str) -> (Token, int):
    # parser, parser_value, parser_position
    scores = [(parser, *parser(text)) for parser in TokenType.parsers]
    # sort by position descending
    scores.sort(key=lambda x: -x[2])
    if scores[0][2] == 0:
        # everything failed to parse
        raise TypeError
    else:
        return Token(scores[0][0].__self__, scores[0][1]), scores[0][2]
