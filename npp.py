def safe_float(input_str, prompt=None):
    """
    Safely convert input to float, repeatedly prompt until valid.
    """
    while True:
        value = input(input_str if prompt is None else prompt)
        try:
            return float(value)
        except ValueError:
            print("Invalid number, please try again.")

def get_n_floats(n, label):
    """
    Get n floats from user input with a label.
    """
    arr = []
    for i in range(n):
        arr.append(safe_float(f"Enter {label} for group {i+1}: "))
    return arr

def print_formula_result(formula, value, error=None):
    """
    Standardized formula + result display.
    """
    if error:
        print(f"{formula} => Error: {error}")
    else:
        print(f"{formula} => {value}")
