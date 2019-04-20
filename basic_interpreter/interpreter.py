from typing import Type

from .basic import Token, TokenType, infer_type


class Interpreter:

    def __init__(self, text: str):
        self.text = text

    def __call__(self):
        return self._evaluate()

    def _evaluate(self):
        tokens = []

        pos = 0
        while True:
            next_token, next_pos = self._parse_next_token(self.text, pos)
            tokens.append(next_token)
            pos = next_pos
            if pos >= len(self.text):
                break

        return tokens

    def _infer_type(self, text: str) -> Type[TokenType]:
        return infer_type(text)

    def _parse_next_token(self, text: str, pos: int) -> (Type[TokenType], int):
        type_ = self._infer_type(text[pos:])
        value, pos_ = type_.parse(text[pos:])
        assert pos_ > 0, 'Type cast / parse mismatch'
        pos += pos_
        return Token(type_, value), pos


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
