from .basic import Token, parse, INTEGER, OperatorTokenType


class Lexer:
    def __init__(self, text: str):
        self.pos = 0
        self.text = text

    def __iter__(self):
        return self

    def __next__(self):
        if self.pos >= len(self.text):
            raise StopIteration
        token, rel_pos = parse(self.text[self.pos :])
        self.pos += rel_pos
        return token


class Interpreter:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer

    def __call__(self):
        return self._evaluate()

    def _evaluate(self) -> Token:
        """Evaluates the contents of self.text."""
        # read all tokens into an RPN stack --- shunting-yard algorithm
        rpn_stack = []
        operator_stack = []
        for token in self.lexer:
            if token.type_ is INTEGER:
                rpn_stack.append(token)
            elif issubclass(token.type_, OperatorTokenType):
                rpn_stack.extend(operator_stack)
                operator_stack.clear()
                operator_stack.append(token)
            else:
                raise TypeError
        rpn_stack.extend(operator_stack)

        # evaluate the RPN stack
        operand_stack = []
        for token in rpn_stack:
            if issubclass(token.type_, OperatorTokenType):
                try:
                    right = operand_stack.pop()
                    left = operand_stack.pop()
                except IndexError:
                    raise TypeError

                result = token(left, right)
                operand_stack.append(result)
            elif token.type_ is INTEGER:
                operand_stack.append(token)
            else:
                raise TypeError

        result = operand_stack.pop()
        return result


def main():
    while True:
        try:
            user_input = input("BASIC> ")
        except EOFError:
            break

        if user_input.strip() == "":
            continue

        interpreter = Interpreter(Lexer(user_input))
        result = interpreter()
        print(result)


if __name__ == "__main__":
    main()
