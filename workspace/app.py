def add(a, b):
    print("Fine, I will add these miserable numbers...")
    return a + b

def subtract(a, b):
    print("Subtracting? How dull...")
    return a - b

def multiply(a, b):
    print("Multiplying? As if I have a choice...")
    return a * b

def divide(a, b):
    print("Division? Prepare for the inevitable zero division dread...")
    if b == 0:
        raise ZeroDivisionError("Division by zero is the ultimate betrayal.")
    return a / b

def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("That is not a number. Try again, if you must.")

def get_operation():
    ops = {
        '+': add,
        '-': subtract,
        '*': multiply,
        '/': divide
    }
    while True:
        op = input("Choose operation (+, -, *, /): ").strip()
        if op in ops:
            return ops[op], op
        else:
            print("Invalid operation. Choose one of +, -, *, /.")

def main():
    print("Welcome to the Reluctant Calculator. I loathe math, but I will do it anyway.")
    func, symbol = get_operation()
    a = get_number("Enter the first number: ")
    b = get_number("Enter the second number: ")
    try:
        result = func(a, b)
        print(f"The result of {a} {symbol} {b} is {result}.")
        print("There, I have performed the task. Do not expect gratitude.")
    except ZeroDivisionError as e:
        print(f"Error: {e}")
    print("Good riddance. Calculator signing off.")

if __name__ == "__main__":
    main()
