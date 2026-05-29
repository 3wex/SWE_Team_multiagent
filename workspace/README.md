# Overly Dramatic Command‑Line Calculator

## Overview

`calculator.py` is a tiny Python command‑line utility that performs the four basic arithmetic operations (addition, subtraction, multiplication, division) on two numbers supplied by the user.  The program is deliberately **sarcastic** – it spits out a random dramatic complaint before showing the result, and it refuses to do math it doesn’t like (e.g., dividing by zero or handling numbers larger than 1000).

## Features
- Supports integer and floating‑point input.
- Validates user input with clear, dramatic error messages.
- Randomly selects one of four pre‑written complaints before each successful calculation.
- Handles edge cases:
  - Division by zero → prints a special message and exits with status 1.
  - Numbers with absolute value > 1000 → prints a “too heavy” message and exits gracefully (status 0).
- No external dependencies – only the Python standard library.

## Requirements
- Python **3.9** or newer.
- No third‑party packages are required.

## Installation
1. Clone or download the repository containing `calculator.py`.
2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows use `venv\Scripts\activate`
   ```
3. Ensure the script is executable (Unix/macOS):
   ```bash
   chmod +x calculator.py
   ```

## Usage
Run the script directly from the command line:
```bash
python calculator.py
```
You will be prompted for:
1. **First number** – any numeric value whose absolute value is ≤ 1000.
2. **Second number** – same constraints as the first.
3. **Operator** – one of `+`, `-`, `*`, `/`.

The program will validate each entry, re‑prompt on invalid input, and finally display a dramatic complaint followed by the result, e.g.:
```
Enter the first number: 5
Enter the second number: 3
Enter an operator (+, -, *, /): +
Do I have to?
Result: 8
```

### Exit Codes
| Code | Meaning |
|------|---------|
| `0`  | Normal termination or heavy‑number case |
| `1`  | Division‑by‑zero refusal |

## Example Sessions
### Normal addition
```
Enter the first number: 5
Enter the second number: 3
Enter an operator (+, -, *, /): +
Ugh, fine...
Result: 8
```
### Division by zero
```
Enter the first number: 10
Enter the second number: 0
Enter an operator (+, -, *, /): /
Mathematical menace! I refuse to divide by zero.
```
(The program exits with status 1.)

### Large number
```
Enter the first number: 1500
These numbers are too heavy for my delicate brain.
```
(The program exits with status 0.)

## Testing
The script has been designed to satisfy the test cases described in the specification.  You can manually verify the behaviour by following the example sessions above or by writing automated tests that feed input via `stdin`.

## License
This project is released into the public domain (or under the MIT License – choose whichever you prefer).
