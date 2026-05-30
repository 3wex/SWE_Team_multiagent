import sys
import unittest

def dramatic_message_before(operation: str) -> str:
    """Return a unique dramatic message before performing the given operation."""
    messages = {
        "add": "Alas, I must endure the torment of addition...",
        "subtract": "With great reluctance I approach subtraction, a bleak affair...",
        "multiply": "Multiplication looms before me like a storm of dread...",
        "divide": "Division, the most heinous of tasks, beckons me..."
    }
    return messages.get(operation, "I am forced to perform an unknown operation...")

def dramatic_message_after() -> str:
    """Return a dramatic relief message after a calculation."""
    return "At last, the ordeal is over, and I can breathe again."

def calculate(a: float, b: float, operation: str) -> float:
    """Perform the arithmetic operation and return the result.

    Raises:
        ZeroDivisionError: If division by zero is attempted.
        ValueError: If an unsupported operation is provided.
    """
    if operation == "add":
        return a + b
    if operation == "subtract":
        return a - b
    if operation == "multiply":
        return a * b
    if operation == "divide":
        if b == 0:
            raise ZeroDivisionError
        return a / b
    raise ValueError("Unsupported operation")

def parse_operation(op_input: str) -> str:
    """Map user input to internal operation keyword."""
    mapping = {
        "+": "add",
        "add": "add",
        "-": "subtract",
        "subtract": "subtract",
        "*": "multiply",
        "multiply": "multiply",
        "/": "divide",
        "divide": "divide"
    }
    return mapping.get(op_input.lower())

def main() -> None:
    print("Behold, I am summoned to perform mathematics, a task I dread beyond measure.")
    while True:
        try:
            a_input = input("Enter the first number: ")
            a = float(a_input)
        except Exception:
            print("Disgust fills me at your incompetence with numbers. Farewell.")
            sys.exit(1)
            return
        try:
            b_input = input("Enter the second number: ")
            b = float(b_input)
        except Exception:
            print("Disgust fills me at your incompetence with numbers. Farewell.")
            sys.exit(1)
            return
        op_input = input("Enter operation (+, -, *, /): ")
        operation = parse_operation(op_input)
        if operation is None:
            print("Your choice of operation is an affront to my sensibilities. Farewell.")
            sys.exit(1)
            return
        print(dramatic_message_before(operation))
        try:
            result = calculate(a, b, operation)
        except ZeroDivisionError:
            print("Horror! You dare ask me to divide by zero, an atrocious act! I shall not comply.")
            sys.exit(1)
            return
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            sys.exit(1)
            return
        print(f"Result: {result}")
        print(dramatic_message_after())
        again = input("Do you wish to perform another calculation? (yes/no): ")
        if again.strip().lower() not in ["yes", "y"]:
            print("Very well, I retire from this miserable chore.")
            break

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(calculate(2, 3, "add"), 5)

    def test_subtract(self):
        self.assertEqual(calculate(5, 2, "subtract"), 3)

    def test_multiply(self):
        self.assertEqual(calculate(4, 3, "multiply"), 12)

    def test_divide(self):
        self.assertAlmostEqual(calculate(10, 2, "divide"), 5)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculate(1, 0, "divide")

    def test_invalid_operation(self):
        with self.assertRaises(ValueError):
            calculate(1, 2, "mod")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run unit tests and force output to stdout
        unittest.main(argv=[sys.argv[0]], exit=False, verbosity=2,
                      testRunner=unittest.TextTestRunner(stream=sys.stdout))
    else:
        main()
