from toolkit.errors import CalculatorError


def tokenize(expression: str) -> list:
    if not expression or expression.strip() == "":
        raise CalculatorError("Пустое выражение")

    expression = expression.replace(" ","")

    tokens = []
    i = 0
    n = len(expression)

    while i < n:
        current_char = expression[i]

        if current_char.isdigit() or current_char == '.':
            token = ""
            dot = False

            while i < n and (expression[i].isdigit() or expression[i] == '.'):
                if expression[i] == '.':
                    if dot:
                        raise CalculatorError("Неверное числовое значение")
                    dot = True
                token += expression[i]
                i += 1

            if token == "" or token.startswith(".") or token.endswith("."):
                raise CalculatorError("Неверное числовое значение")

            tokens.append(float(token))
            continue


        elif current_char in ('+','*','/','-'):
            tokens.append(current_char)
            i += 1
            continue
        else:
            raise CalculatorError(f"Недопустимый символ: {current_char}")

    res_tokens = []
    x=0
    count_tokens = len(tokens)

    while x < count_tokens:
        token = tokens[x]

        unary = (token in ('+','-')) and (x == 0 or isinstance(res_tokens[-1], str))

        if unary:
            if x + 1 < count_tokens and isinstance(tokens[x+1], (int, float)):
                next_number = tokens[x+1]

                if token == '-':
                    next_number = -next_number
                res_tokens.append(next_number)
                x+=2
                continue
            else:
                raise CalculatorError("Пропущенный операнд")

        res_tokens.append(token)
        x+=1
    return res_tokens


def to_rpn(tokens: list) -> list:
    priorities = {'+':1, '-':1, '*':2, '/':2}
    res_rpn = []
    stack = []

    for token in tokens:
        if isinstance(token, (int, float)):
            res_rpn.append(token)

        elif token in priorities:
            while stack and priorities.get(stack[-1], 0) >= priorities[token]:
                res_rpn.append(stack.pop())

            stack.append(token)

    while stack:
        res_rpn.append(stack.pop())

    return res_rpn

def calculate_rpn(rpn_tokens: list) -> float:
    stack = []

    for token in rpn_tokens:
        if isinstance(token, (int, float)):
            stack.append(token)

        elif token in ('+', '-', '*', '/'):
            if len(stack) < 2:
                raise CalculatorError("Пропущенный операнд")

            b = stack.pop()
            a = stack.pop()

            if token == '+':
                stack.append(a+b)
            elif token == '-':
                stack.append(a-b)
            elif token == '*':
                stack.append(a*b)
            elif token == '/':
                if b == 0:
                    raise CalculatorError("Деление на ноль")
                stack.append(a/b)

    if len(stack) != 1:
        raise CalculatorError("Пропущенный операнд")

    return float(stack[0])

def calculate(expression: str) -> float:

    tokens = tokenize(expression)

    for i in range(len(tokens) - 1):
        if isinstance(tokens[i], str) and isinstance(tokens[i+1], str):
            raise CalculatorError("Два бинарных оператора подряд")

    rpn_tokens = to_rpn(tokens)

    return calculate_rpn(rpn_tokens)

