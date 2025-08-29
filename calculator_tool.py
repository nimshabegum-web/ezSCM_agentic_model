def add(a, b): 
    return a + b

def subtract(a, b): 
    return a - b

def multiply(a, b): 
    return a * b

def divide(a, b): 
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b

def calculate(expression: str):
    """
    Evaluates simple symbolic math expressions with +, -, *, /
    Examples:
      - "12 * 7"
      - "45 + 30"
      - "100 / 5"
      - "20 - 7"
    """
    expression = expression.strip()

    # Only allow digits, operators, spaces, and decimal points
    for ch in expression:
        if not (ch.isdigit() or ch.isspace() or ch in "+-*/()."):
            raise ValueError(f"Invalid character in expression: {ch}")

    import re
    match = re.match(r"^\s*(-?\d+(?:\.\d+)?)\s*([\+\-\*/])\s*(-?\d+(?:\.\d+)?)\s*$", expression)
    if not match:
        raise ValueError(f"Unsupported calculation format: {expression}")

    a, op, b = float(match.group(1)), match.group(2), float(match.group(3))

    if op == "+": return add(a, b)
    if op == "-": return subtract(a, b)
    if op == "*": return multiply(a, b)
    if op == "/": return divide(a, b)

    raise ValueError(f"Unsupported operator: {op}")
