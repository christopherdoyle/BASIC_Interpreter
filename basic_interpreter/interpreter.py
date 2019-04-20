from typing import Type

from .basic import Token, TokenType, parse


class Interpreter:

    def __init__(self, text: str):
        self.text = text

    def __call__(self):
        return self._evaluate()

    def _evaluate(self):
        tokens = []

        pos = 0
        while True:
            next_token, next_pos = parse(self.text[pos:])
            tokens.append(next_token)
            pos += next_pos
            if pos >= len(self.text):
                break

        return tokens


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
