import sys
import argparse
import re
import operator
import unittest

# Mapping of operators to functions
_OPERATORS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}

_HELP_MESSAGE = """Usage: python calc.py [options]

Options:
  -e, --expr "<expression>"   Evaluate a single expression and exit.
  -v, --verbose               Show parsed expression before evaluation.
  -h, --help                  Show this help message and exit.

Supported operators: +  -  *  /
Examples:
  calc> 2 + 3
  5
  python calc.py -e "10 / 2"
  5
"""

def _remove_exponent_parts(expr: str) -> str:
    """Remove scientific notation exponent parts to avoid counting their signs as operators."""
    return re.sub(r'[eE][\+\-]?\d+', '', expr)

def _count_operators(expr: str) -> int:
    cleaned = _remove_exponent_parts(expr)
    return len(re.findall(r'[\+\-\*/]', cleaned))

def _find_operator(expr: str) -> str | None:
    cleaned = _remove_exponent_parts(expr)
    ops = re.findall(r'[\+\-\*/]', cleaned)
    return ops[0] if ops else None

def _parse_expression(expr: str):
    """Parse a binary arithmetic expression.

    Returns:
        (operand1: float, operator: str, operand2: float) on success,
        (error_message: str, None, None) on failure.
    """
    if not expr.strip():
        return None, None, None  # Empty line

    # Check for invalid characters
    if re.search(r'[^\d\s\.\+\-\*/eE]', expr):
        return "Error: Invalid characters in expression", None, None

    # Count operators (excluding exponent signs)
    op_count = _count_operators(expr)
    if op_count == 0:
        return "Error: Missing operand or operator", None, None
    if op_count > 1:
        return "Error: Only single binary operations are supported", None, None

    # Identify the operator
    op = _find_operator(expr)
    if op not in _OPERATORS:
        return f"Error: Unsupported operator '{op}'", None, None

    # Split operands around the operator
    # Use a regex that respects possible spaces
    pattern = rf'^\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)\s*\{re.escape(op)}\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)\s*$'
    match = re.match(pattern, expr)
    if not match:
        # Could be missing operand or malformed number
        return "Error: Missing operand or operator", None, None

    left_str, right_str = match.group(1), match.group(2)

    try:
        left = float(left_str)
        right = float(right_str)
    except ValueError:
        return "Error: Invalid numeric operand", None, None

    return left, op, right

def _format_result(value):
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)

def evaluate(expr: str, verbose: bool = False):
    parsed = _parse_expression(expr)
    if parsed[0] is None and parsed[1] is None and parsed[2] is None:
        # Empty line – no output
        return None, 0
    if isinstance(parsed[0], str) and parsed[1] is None:
        # Error message returned
        return parsed[0], 1
    left, op, right = parsed
    if verbose:
        print(f"Parsed: {left} {op} {right}")
    try:
        if op == '/' and right == 0:
            return "Error: Division by zero", 1
        result = _OPERATORS[op](left, right)
        return _format_result(result), 0
    except ZeroDivisionError:
        return "Error: Division by zero", 1

def interactive_mode(verbose: bool):
    while True:
        try:
            line = input("calc> ")
        except EOFError:
            print()  # Newline on Ctrl-D
            break
        except KeyboardInterrupt:
            print("\nInterrupted – exiting")
            break

        line = line.strip()
        if line.lower() in ("exit", "quit"):
            break
        if not line:
            continue

        output, code = evaluate(line, verbose)
        if output is not None:
            print(output)
        if code != 0 and not verbose:
            # In interactive mode we continue even after errors
            continue

def main():
    parser = argparse.ArgumentParser(add_help=False, prog='calc.py')
    parser.add_argument('-e', '--expr', type=str, help='Expression to evaluate')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-h', '--help', action='store_true', help='Show help')
    parser.add_argument('--test', action='store_true', help=argparse.SUPPRESS)

    args, unknown = parser.parse_known_args()
    if unknown:
        print(_HELP_MESSAGE)
        sys.exit(2)

    if args.help:
        print(_HELP_MESSAGE)
        sys.exit(0)

    if args.test:
        # Run unit tests
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(CalcTests)
        runner = unittest.TextTestRunner()
        result = runner.run(suite)
        sys.exit(0 if result.wasSuccessful() else 1)

    if args.expr is not None:
        output, code = evaluate(args.expr, args.verbose)
        if output is not None:
            print(output)
        sys.exit(code)

    # Interactive mode
    try:
        interactive_mode(args.verbose)
    except KeyboardInterrupt:
        print("\nInterrupted – exiting")
        sys.exit(0)

# Unit Tests
class CalcTests(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(evaluate("2 + 3")[0], "5")

    def test_subtraction(self):
        self.assertEqual(evaluate("5 - 2")[0], "3")

    def test_multiplication(self):
        self.assertEqual(evaluate("-4 * 2.5")[0], "-10")

    def test_division(self):
        self.assertEqual(evaluate("7 / 2")[0], "3.5")

    def test_divide_by_zero(self):
        out, code = evaluate("5 / 0")
        self.assertEqual(out, "Error: Division by zero")
        self.assertEqual(code, 1)

    def test_invalid_operator(self):
        out, code = evaluate("5 ^ 2")
        self.assertEqual(out, "Error: Unsupported operator '^'")
        self.assertEqual(code, 1)

    def test_invalid_operand(self):
        out, code = evaluate("a + 2")
        self.assertEqual(out, "Error: Invalid numeric operand")
        self.assertEqual(code, 1)

    def test_missing_operand(self):
        out, code = evaluate("5 +")
        self.assertEqual(out, "Error: Missing operand or operator")
        self.assertEqual(code, 1)

    def test_multiple_operators(self):
        out, code = evaluate("3 + 4 - 2")
        self.assertEqual(out, "Error: Only single binary operations are supported")
        self.assertEqual(code, 1)

    def test_scientific_notation(self):
        self.assertEqual(evaluate("1e3 * 2")[0], "2000")

    def test_whitespace_variations(self):
        self.assertEqual(evaluate("   3   +4   ")[0], "7")

    def test_invalid_characters(self):
        out, code = evaluate("3 $ 4")
        self.assertEqual(out, "Error: Invalid characters in expression")
        self.assertEqual(code, 1)

    def test_empty_input(self):
        out, code = evaluate("")
        self.assertIsNone(out)
        self.assertEqual(code, 0)

if __name__ == "__main__":
    main()

