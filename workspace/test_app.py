import unittest
import builtins
from unittest.mock import patch
import sys
import io

import app

class TestDramaticCalculator(unittest.TestCase):
    def test_dramatic_message_before_valid(self):
        self.assertEqual(app.dramatic_message_before('add'), "Alas, I must endure the torment of addition...")
        self.assertEqual(app.dramatic_message_before('subtract'), "With great reluctance I approach subtraction, a bleak affair...")
        self.assertEqual(app.dramatic_message_before('multiply'), "Multiplication looms before me like a storm of dread...")
        self.assertEqual(app.dramatic_message_before('divide'), "Division, the most heinous of tasks, beckons me...")
        self.assertEqual(app.dramatic_message_before('unknown'), "I am forced to perform an unknown operation...")

    def test_dramatic_message_after(self):
        self.assertEqual(app.dramatic_message_after(), "At last, the ordeal is over, and I can breathe again.")

    def test_parse_operation(self):
        self.assertEqual(app.parse_operation('+'), 'add')
        self.assertEqual(app.parse_operation('add'), 'add')
        self.assertEqual(app.parse_operation('-'), 'subtract')
        self.assertEqual(app.parse_operation('subtract'), 'subtract')
        self.assertEqual(app.parse_operation('*'), 'multiply')
        self.assertEqual(app.parse_operation('multiply'), 'multiply')
        self.assertEqual(app.parse_operation('/'), 'divide')
        self.assertEqual(app.parse_operation('divide'), 'divide')
        self.assertIsNone(app.parse_operation('mod'))

    def test_calculate_operations(self):
        self.assertEqual(app.calculate(2, 3, 'add'), 5)
        self.assertEqual(app.calculate(5, 2, 'subtract'), 3)
        self.assertEqual(app.calculate(4, 3, 'multiply'), 12)
        self.assertAlmostEqual(app.calculate(10, 2, 'divide'), 5)
        with self.assertRaises(ZeroDivisionError):
            app.calculate(1, 0, 'divide')
        with self.assertRaises(ValueError):
            app.calculate(1, 2, 'mod')

    @patch('builtins.input', side_effect=['a', '1', '1', '+', 'no'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_non_numeric_first_input_exits(self, mock_stdout, mock_input):
        with self.assertRaises(SystemExit) as cm:
            app.main()
        self.assertEqual(cm.exception.code, 1)
        output = mock_stdout.getvalue()
        self.assertIn('Disgust fills me at your incompetence with numbers', output)

    @patch('builtins.input', side_effect=['1', 'b', '1', '+', 'no'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_non_numeric_second_input_exits(self, mock_stdout, mock_input):
        with self.assertRaises(SystemExit) as cm:
            app.main()
        self.assertEqual(cm.exception.code, 1)
        output = mock_stdout.getvalue()
        self.assertIn('Disgust fills me at your incompetence with numbers', output)

    @patch('builtins.input', side_effect=['1', '2', 'mod', 'no'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_invalid_operation_exits(self, mock_stdout, mock_input):
        with self.assertRaises(SystemExit) as cm:
            app.main()
        self.assertEqual(cm.exception.code, 1)
        output = mock_stdout.getvalue()
        self.assertIn('Your choice of operation is an affront to my sensibilities', output)

    @patch('builtins.input', side_effect=['4', '0', '/', 'no'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_divide_by_zero_exits(self, mock_stdout, mock_input):
        with self.assertRaises(SystemExit) as cm:
            app.main()
        self.assertEqual(cm.exception.code, 1)
        output = mock_stdout.getvalue()
        self.assertIn('Horror! You dare ask me to divide by zero', output)

    @patch('builtins.input', side_effect=['3', '5', '+', 'no'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_successful_addition(self, mock_stdout, mock_input):
        # Should not raise SystemExit because user says no to another calculation
        app.main()
        output = mock_stdout.getvalue()
        self.assertIn('Result: 8.0', output)
        self.assertIn(app.dramatic_message_before('add'), output)
        self.assertIn(app.dramatic_message_after(), output)

if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)
