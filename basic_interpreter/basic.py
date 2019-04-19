from enum import Enum


class TokenType(Enum):
    INTEGER = 1


class Token:

    def __init__(self, type_, value):
        self.type_ = type_
        self.value = value

    def __str__(self):
        if self.value is None:
            return self.type_.name
        else:
            return f'{self.type_.name}:{self.value}'

    def __repr__(self):
        return self.__str__()
