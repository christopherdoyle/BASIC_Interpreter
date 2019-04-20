from typing import Type


class TokenType:

    name = None
    casts = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.casts.append(cls.cast)

    @classmethod
    def cast(cls, value):
        raise NotImplementedError

    @classmethod
    def add(cls, left, right):
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
    def cast(cls, value):
        return int(value)

    def add(self, left: int, right: int) -> int:
        return left + right


class OPERATOR(TokenType):

    @classmethod
    def __call__(cls, left, right):
        raise NotImplementedError


class PLUS(OPERATOR):

    name = '+'

    @classmethod
    def __call__(cls, left: Token, right: Token):
        return left + right

    @classmethod
    def cast(cls, value):
        if value == '+':
            return value
        else:
            raise ValueError


def try_cast(value) -> Type[TokenType]:
    for cast in TokenType.casts:
        try:
            cast(value)
            break
        except:
            continue
    else:
        raise TypeError

    return cast.__self__
