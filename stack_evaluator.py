import sys
class Stack:
    """A simple stack (LIFO: last in, first out) backed by a Python list."""

    def __init__(self):
        self._items = []

    def push(self, item):
        """Add an item to the top of the stack."""
        self._items.append(item)

    def pop(self):
        """Remove and return the top item."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        """Return the top item without removing it."""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)
def precedence(op):
    """Higher number = evaluated first."""
    if op in ("+", "-"):
        return 1
    if op in ("*", "/"):
        return 2
    return 0


def tokenize(expression):
    """Break a string like '(8 / 4) + 7' into numbers, operators and brackets."""
    tokens = []
    i = 0
    while i < len(expression):
        ch = expression[i]
        if ch.isspace():
            i += 1
        elif ch.isdigit() or ch == ".":
            start = i
            while i < len(expression) and (expression[i].isdigit() or expression[i] == "."):
                i += 1
            tokens.append(float(expression[start:i]))
        elif ch in "+-*/()":
            tokens.append(ch)
            i += 1
        else:
            raise ValueError(f"Invalid character: {ch}")
    return tokens


def apply_operator(numbers, operators):
    """Pop one operator and two numbers, calculate, push the result back."""
    op = operators.pop()
    right = numbers.pop()
    left = numbers.pop()
    if op == "+":
        numbers.push(left + right)
    elif op == "-":
        numbers.push(left - right)
    elif op == "*":
        numbers.push(left * right)
    elif op == "/":
        if right == 0:
            raise ZeroDivisionError("Division by zero")
        numbers.push(left / right)


def evaluate_expression(expression):
    """Evaluate a math expression using two stacks."""
    numbers = Stack()
    operators = Stack()

    for token in tokenize(expression):
        if isinstance(token, float):
            numbers.push(token)
        elif token == "(":
            operators.push(token)
        elif token == ")":
            while not operators.is_empty() and operators.peek() != "(":
                apply_operator(numbers, operators)
            if operators.is_empty():
                raise ValueError("Mismatched parentheses")
            operators.pop()  # discard the "("
        else:  # + - * /
            while (not operators.is_empty()
                   and operators.peek() != "("
                   and precedence(operators.peek()) >= precedence(token)):
                apply_operator(numbers, operators)
            operators.push(token)

    while not operators.is_empty():
        if operators.peek() == "(":
            raise ValueError("Mismatched parentheses")
        apply_operator(numbers, operators)

    if numbers.size() != 1:
        raise ValueError("Invalid expression")
    return numbers.pop()


def format_result(value):
    """Show 13.0 as 13, but keep 2.5 as 2.5."""
    if value == int(value):
        return str(int(value))
    return str(round(value, 4))
def is_separator(line):
    """A separator line contains only dashes, like -----"""
    stripped = line.strip()
    return len(stripped) >= 3 and set(stripped) == {"-"}


def read_expressions(input_path):
    """Read input.txt. Returns (expressions, separator_used)."""
    expressions = []
    separator = "-----"  # default if the file has none
    found_separator = False

    with open(input_path, "r") as f:
        for line in f:
            text = line.strip()
            if text == "":
                continue  # skip blank lines
            if is_separator(text):
                if not found_separator:
                    separator = text  # remember the style used in the input
                    found_separator = True
            else:
                expressions.append(text)

    return expressions, separator


def process_file(input_path, output_path):
    """Evaluate every expression in input_path and write results to output_path."""
    expressions, separator = read_expressions(input_path)

    results = []
    for expr in expressions:
        try:
            results.append(format_result(evaluate_expression(expr)))
        except ZeroDivisionError:
            results.append("Error: division by zero")
        except (ValueError, IndexError):
            results.append("Error: invalid expression")

    with open(output_path, "w") as f:
        f.write(("\n" + separator + "\n").join(results) + "\n")

    return results

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output.txt"
    results = process_file(input_file, output_file)
    for r in results:
        print(r)
    print(f"Done. Results written to {output_file}")