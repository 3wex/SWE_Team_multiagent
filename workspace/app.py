import sys
import random

# Set a fixed seed for reproducibility of random complaint selection
random.seed(0)

COMPLAINTS = [
    "Ugh, fine...",
    "Do I have to?",
    "You couldn't do this in your head?",
    "Why am I even here?",
]

HEAVY_NUMBER_MSG = "These numbers are too heavy for my delicate brain."
DIVIDE_BY_ZERO_MSG = "Mathematical menace! I refuse to divide by zero."

def get_number(prompt: str) -> float:
    while True:
        try:
            raw = input(prompt)
        except EOFError:
            # End of input stream; exit gracefully
            sys.exit(0)
        raw = raw.strip()
        if not raw:
            print("Whoa, that's not a number! Try again.")
            continue
        try:
            value = float(raw)
        except ValueError:
            print("Whoa, that's not a number! Try again.")
            continue
        # Large number check
        if abs(value) > 1000:
            print(HEAVY_NUMBER_MSG)
            sys.exit(0)
        return value

def get_operator(prompt: str) -> str:
    valid_ops = {"+", "-", "*", "/"}
    while True:
        try:
            raw = input(prompt)
        except EOFError:
            sys.exit(0)
        raw = raw.strip()
        if raw not in valid_ops:
            print("Seriously? That's not an operator.")
            continue
        return raw

def main():
    first = get_number("Enter the first number:")
    second = get_number("Enter the second number:")
    op = get_operator("Enter an operator (+, -, *, /):")

    # Division by zero handling
    if op == "/" and second == 0:
        print(DIVIDE_BY_ZERO_MSG)
        sys.exit(1)

    # Dramatic complaint (once per successful calculation)
    complaint = random.choice(COMPLAINTS)
    print(complaint)

    # Perform calculation
    if op == "+":
        result = first + second
    elif op == "-":
        result = first - second
    elif op == "*":
        result = first * second
    elif op == "/":
        result = first / second
    else:
        # Should never happen due to validation
        print("Unexpected operator.")
        sys.exit(1)

    # Format result: drop .0 for whole numbers
    if isinstance(result, float) and result.is_integer():
        result_str = str(int(result))
    else:
        result_str = str(result)

    print(f"Result: {result_str}")

if __name__ == "__main__":
    main()
