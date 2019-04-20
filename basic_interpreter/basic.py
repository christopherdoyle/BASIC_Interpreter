from typing import Type


class TokenType:

    name = None

    @classmethod
    def cast(cls, value):
        raise NotImplementedError


class INTEGER(TokenType):

    name = 'INTEGER'

    @classmethod
    def cast(cls, value):
        return int(value)


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

    def __eq__(self, other):
        return self.type_ == other.type_ and self.value == other.value
