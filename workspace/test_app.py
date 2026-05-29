import builtins
import sys
import io
import unittest
from unittest.mock import patch

import app

class TestCalculator(unittest.TestCase):
    def run_app_with_inputs(self, inputs):
        """Helper to run app.main() with a list of inputs.
        Returns a tuple (output, exit_code). exit_code is None if no SystemExit.
        """
        with patch.object(builtins, 'input', side_effect=inputs):
            captured_out = io.StringIO()
            sys_stdout = sys.stdout
            sys.stdout = captured_out
            try:
                app.main()
                exit_code = None
            except SystemExit as e:
                exit_code = e.code
            finally:
                sys.stdout = sys_stdout
            return captured_out.getvalue(), exit_code

    def test_normal_addition(self):
        out, code = self.run_app_with_inputs(['5', '3', '+'])
        self.assertIsNone(code)
        lines = [line.strip() for line in out.strip().split('\n') if line.strip()]
        self.assertIn('Result: 8', lines)
        complaints = set(app.COMPLAINTS)
        self.assertTrue(any(line in complaints for line in lines), f"No complaint found in {lines}")

    def test_division_by_zero(self):
        out, code = self.run_app_with_inputs(['10', '0', '/'])
        self.assertEqual(code, 1)
        self.assertIn(app.DIVIDE_BY_ZERO_MSG, out)

    def test_large_number_exit(self):
        out, code = self.run_app_with_inputs(['1500', '2', '*'])
        self.assertEqual(code, 0)
        self.assertIn(app.HEAVY_NUMBER_MSG, out)

    def test_invalid_operator_reprompt(self):
        out, code = self.run_app_with_inputs(['4', '5', 'x', '+'])
        self.assertIsNone(code)
        lines = [line.strip() for line in out.strip().split('\n') if line.strip()]
        self.assertIn("Seriously? That's not an operator.", lines)
        self.assertIn('Result: 9', lines)

    def test_non_numeric_first_number(self):
        out, code = self.run_app_with_inputs(['abc', '7', '2', '+'])
        self.assertIsNone(code)
        lines = [line.strip() for line in out.strip().split('\n') if line.strip()]
        self.assertIn("Whoa, that's not a number! Try again.", lines)
        self.assertIn('Result: 9', lines)

    def test_negative_large_number_exit(self):
        out, code = self.run_app_with_inputs(['-2000', '5', '-'])
        self.assertEqual(code, 0)
        self.assertIn(app.HEAVY_NUMBER_MSG, out)

if __name__ == '__main__':
    unittest.main(exit=False)
