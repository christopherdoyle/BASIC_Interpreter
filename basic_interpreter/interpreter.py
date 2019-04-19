from .basic import Token


class Interpreter:

    def __init__(self, text):
        self.text = text

    def __call__(self):
        return self._evaluate()

    def _evaluate(self):
        pass


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
