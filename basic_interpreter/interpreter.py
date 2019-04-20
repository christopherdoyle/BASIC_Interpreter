from typing import Type

from .basic import Token, TokenType, INTEGER


class Interpreter:

    def __init__(self, text: str):
        self.text = text

    def __call__(self):
        return self._evaluate()

    def _evaluate(self):
        type_ = self._infer_type(self.text)
        value = self._cast_value(self.text, type_)
        return Token(type_, value)

    def _infer_type(self, text: str) -> Type[TokenType]:
        if text.isdigit():
            return INTEGER
        else:
            raise NotImplementedError

    def _cast_value(self, value, type_: Type[TokenType]):
        return type_.cast(value)


def main():
    while True:
        try:
            user_input = input('BASIC> ')
        except EOFError:
            break

        if user_input.strip() == '':
            continue

        interpreter = Interpreter(user_input)
        result = interpreter()
        print(result)


if __name__ == '__main__':
    main()
