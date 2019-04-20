from .basic import Token, parse, INTEGER, OPERATOR


class Lexer:

    def __init__(self, text: str):
        self.text = text

    def parse_tokens(self):
        return list(self.parse_tokens_iter())

    def parse_tokens_iter(self):
        """Read all tokens from the input string, left-to-right."""
        pos = 0
        while True:
            next_token, next_pos = parse(self.text[pos:])
            yield next_token
            pos += next_pos
            if pos >= len(self.text):
                break


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
        for token in self.lexer.parse_tokens_iter():
            if token.type_ is INTEGER:
                rpn_stack.append(token)
            elif issubclass(token.type_, OPERATOR):
                rpn_stack.extend(operator_stack)
                operator_stack.clear()
                operator_stack.append(token)
            else:
                raise TypeError
        rpn_stack.extend(operator_stack)

        # evaluate the RPN stack
        operand_stack = []
        for token in rpn_stack:
            if issubclass(token.type_, OPERATOR):
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
            user_input = input('BASIC> ')
        except EOFError:
            break

        if user_input.strip() == '':
            continue

        interpreter = Interpreter(Lexer(user_input))
        result = interpreter()
        print(result)


if __name__ == '__main__':
    main()
