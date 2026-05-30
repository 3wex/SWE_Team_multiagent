import unittest
import builtins
from unittest.mock import patch
import io
import sys
import app

class TestCalculatorFunctions(unittest.TestCase):
    def test_add(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = app.add(2, 3)
            self.assertEqual(result, 5)
            self.assertIn('Fine, I will add these miserable numbers...', fake_out.getvalue())

    def test_subtract(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = app.subtract(10, 4)
            self.assertEqual(result, 6)
            self.assertIn('Subtracting? How dull...', fake_out.getvalue())

    def test_multiply(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = app.multiply(3, 7)
            self.assertEqual(result, 21)
            self.assertIn('Multiplying? As if I have a choice...', fake_out.getvalue())

    def test_divide(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            result = app.divide(8, 2)
            self.assertEqual(result, 4)
            self.assertIn('Division? Prepare for the inevitable zero division dread...', fake_out.getvalue())

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError) as cm:
            app.divide(5, 0)
        self.assertEqual(str(cm.exception), 'Division by zero is the ultimate betrayal.')

    def test_get_number_valid(self):
        with patch('builtins.input', return_value='42'):
            self.assertEqual(app.get_number('Enter: '), 42.0)

    def test_get_number_invalid_then_valid(self):
        inputs = ['abc', '3.14']
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                result = app.get_number('Enter: ')
                self.assertEqual(result, 3.14)
                self.assertIn('That is not a number. Try again, if you must.', fake_out.getvalue())

    def test_get_operation_valid(self):
        with patch('builtins.input', return_value='+'):
            func, symbol = app.get_operation()
            self.assertEqual(func, app.add)
            self.assertEqual(symbol, '+')

    def test_get_operation_invalid_then_valid(self):
        inputs = ['x', '*']
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                func, symbol = app.get_operation()
                self.assertEqual(func, app.multiply)
                self.assertEqual(symbol, '*')
                self.assertIn('Invalid operation. Choose one of +, -, *, /.', fake_out.getvalue())

if __name__ == '__main__':
    # Run tests and print a concise summary
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestCalculatorFunctions)
    runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)
    result = runner.run(suite)
    # Exit with appropriate code (optional)
    sys.exit(not result.wasSuccessful())
