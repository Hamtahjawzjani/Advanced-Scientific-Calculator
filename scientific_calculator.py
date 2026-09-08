# Scientific Calculator Application
import tkinter as tk
import math
import re

# Create the main calculator window
window = tk.Tk()
window.title("Scientific Calculator")
window.geometry("600x800")
window.config(bg="black")

# Main control buttons
control_buttons = ["C", "Del", "Inv", "DEG", "Exp"]

# Supported arithmetic operators
operators = "+-x÷"

# Initial angle mode
angle_mode = "DEG"
angle_mode_changed = False

# Store calculation history
history = []

# Reference to the history frame
history_frame = None

# Scientific calculator visibility state
scientific_visible = False

# Functions and constants that can automatically require multiplication
FUNCTIONS = [
    "sin(",
    "cos(",
    "tan(",
    "cot(",
    "sinh(",
    "cosh(",
    "tanh(",
    "coth(",
    "sin⁻¹(",
    "cos⁻¹(",
    "tan⁻¹(",
    "cot⁻¹(",
    "sinh⁻¹(",
    "cosh⁻¹(",
    "tanh⁻¹(",
    "coth⁻¹(",
    "log(",
    "ln(",
    "e",
    "π",
    "²√(",
    "³√(",
    "abs(",
    "e^(",
    "2^("
]

# Supported numeric characters
NUMBERS = "0123456789"


# Insert a value and automatically add multiplication when necessary
def insert_with_multiplication(value):
    text = expression.get()

    if not text:
        expression.insert(tk.END, value)
        return

    last_char = text[-1]

    previous_is_number = last_char in NUMBERS or last_char == "."
    previous_is_parenthesis = last_char == ")"
    previous_is_constant = last_char in ["e", "π"]

    new_is_number = value and value[0] in NUMBERS
    new_is_parenthesis = value == "("
    new_is_function = value in FUNCTIONS
    new_is_root = value in ["²√(", "³√("]
    new_is_constant = value in ["e", "π"]

    needs_multiplication = False

    if previous_is_number:
        if (
            new_is_parenthesis
            or new_is_function
            or new_is_root
            or new_is_constant
        ):
            needs_multiplication = True

    elif previous_is_parenthesis:
        if (
            new_is_number
            or new_is_parenthesis
            or new_is_function
            or new_is_root
            or new_is_constant
        ):
            needs_multiplication = True

    elif previous_is_constant:
        if (
            new_is_number
            or new_is_parenthesis
            or new_is_function
            or new_is_root
            or new_is_constant
        ):
            needs_multiplication = True

    if needs_multiplication:
        expression.insert(tk.END, "x")

    expression.insert(tk.END, value)


# Add a value or operator to the current expression
def add_to_expression(value):
    if value not in control_buttons:
        text = expression.get()

        if value == "%" and not text:
            return

        # Handle arithmetic operators
        if value in operators:
            if not text:
                return

            if text and text[-1] in operators:
                expression.delete(len(text) - 1, tk.END)
                expression.insert(tk.END, value)
            else:
                expression.insert(tk.END, value)

            return

        insert_with_multiplication(value)


# Clear the current expression and result
def clear():
    expression.delete(0, tk.END)
    result.config(text="")


# Delete the last character from the expression
def Delete():
    text = expression.get()
    new_text = text[:-1]

    expression.delete(0, tk.END)
    expression.insert(0, new_text)


# Calculate cotangent
def cot(x):
    return 1 / math.tan(x)


# Calculate inverse cotangent
def ACOT(x):
    if x > 0:
        return math.atan(1 / x)
    elif x < 0:
        return math.atan(1 / x) + math.pi
    else:
        return math.pi / 2


# Calculate hyperbolic cotangent
def COTH(x):
    return 1 / math.tanh(x)


# Calculate inverse hyperbolic cotangent
def ACOTH(x):
    value = 0.5 * math.log((x + 1) / (x - 1))
    return value


# Find the closing parenthesis corresponding to an opening parenthesis
def find_closing_parenthesis(text, open_index):
    count = 0

    for i in range(open_index, len(text)):
        if text[i] == "(":
            count += 1

        elif text[i] == ")":
            count -= 1

            if count == 0:
                return i

    return -1


# Prepare the expression for Python's eval()
def prepare_expression(text):
    text = text.replace("÷", "/")
    text = text.replace("x", "*")
    text = text.replace("^", "**")
    text = text.replace("π", "math.pi")

    # Convert scientific notation such as 5E2 to 5*10**2
    text = re.sub(
        r'(\d+(?:\.\d+)?)E([+-]?\d+)',
        r'\1*10**\2',
        text
    )

    # Convert the e constant to math.e
    text = re.sub(
        r'(?<![A-Za-z0-9_.])e(?![A-Za-z0-9_])',
        'math.e',
        text
    )

    return text


# Process mathematical functions inside the expression
def process_functions(text):
    functions = {
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "cot": cot,
        "sin⁻¹": math.asin,
        "cos⁻¹": math.acos,
        "tan⁻¹": math.atan,
        "cot⁻¹": ACOT,
        "sinh": math.sinh,
        "cosh": math.cosh,
        "tanh": math.tanh,
        "coth": COTH,
        "sinh⁻¹": math.asinh,
        "cosh⁻¹": math.acosh,
        "tanh⁻¹": math.atanh,
        "coth⁻¹": ACOTH,
        "log": math.log10,
        "ln": math.log,
        "abs": abs,
    }

    # Continue processing until no supported function remains
    while True:
        found_function = False

        for name, function in functions.items():
            search = name + "("
            index = text.rfind(search)

            if index == -1:
                continue

            open_index = index + len(name)
            end = find_closing_parenthesis(text, open_index)

            if end == -1:
                continue

            inside = text[open_index + 1:end]

            # Check whether another function exists inside this function
            has_function_inside = False

            for other_name in functions:
                if other_name + "(" in inside:
                    has_function_inside = True
                    break

            if has_function_inside:
                continue

            answer = eval(prepare_expression(inside))

            # Convert the input angle to radians for DEG mode
            if name in ["sin", "cos", "tan", "cot"]:
                if angle_mode == "DEG":
                    answer = math.radians(answer)

            # Convert inverse trigonometric results back to degrees
            if name in ["sin⁻¹", "cos⁻¹", "tan⁻¹", "cot⁻¹"]:
                value = function(answer)

                if angle_mode == "DEG":
                    value = math.degrees(value)
            else:
                value = function(answer)

            text = text[:index] + str(value) + text[end + 1:]
            found_function = True
            break

        if not found_function:
            break

    return text


# Store the expression that was most recently calculated
last_calculated_expression = None


# Calculate the current expression
def calculate():
    global last_calculated_expression, angle_mode_changed

    original_expression = expression.get()
    text = original_expression

    # Pressing "=" again shows the previous result as the new expression
    if (
        last_calculated_expression is not None
        and text == last_calculated_expression
        and result.cget("text") != ""
        and not angle_mode_changed
    ):
        answer = result.cget("text")

        expression.delete(0, tk.END)
        expression.insert(0, answer)

        result.config(text="")
        last_calculated_expression = None

        return

    try:
        # Automatically close unmatched opening parentheses
        while text.count("(") > text.count(")"):
            text += ")"

        # Process scientific functions
        text = process_functions(text)

        # Convert logarithm functions
        text = text.replace("log", "math.log10")
        text = text.replace("ln", "math.log")

        # Process e^(expression)
        while "e^(" in text:
            start = text.find("e^(")
            end = find_closing_parenthesis(text, start + 2)

            if end == -1:
                break

            inside = text[start + 3:end]

            value = math.exp(
                eval(
                    prepare_expression(inside)
                )
            )

            text = text[:start] + str(value) + text[end + 1:]

        # Process square and cube root functions
        while "²√(" in text or "³√(" in text:
            if "²√(" in text:
                root_symbol = "²√("
                power = 2
            else:
                root_symbol = "³√("
                power = 3

            root_index = text.find(root_symbol)
            start = root_index + len(root_symbol)
            end = start
            count = 0

            while end < len(text):
                if text[end] == "(":
                    count += 1

                elif text[end] == ")":
                    if count == 0:
                        break

                    count -= 1

                end += 1

            number_text = text[start:end]

            if not number_text:
                result.config(text="Invalid input")
                return

            try:
                x = eval(
                    prepare_expression(number_text)
                )
            except ValueError:
                result.config(text="Invalid input")
                return

            if x < 0 and power == 2:
                result.config(text="Invalid input")
                return

            if x < 0 and power == 3:
                value = -((-x) ** (1 / 3))
            else:
                value = x ** (1 / power)

            if end < len(text) and text[end] == ")":
                text = (
                    text[:root_index]
                    + str(value)
                    + text[end + 1:]
                )
            else:
                text = (
                    text[:root_index]
                    + str(value)
                    + text[end:]
                )

        # Process general y√x expressions
        while "√" in text:
            root_index = text.find("√")
            start = root_index - 1

            while start >= 0 and text[start].isdigit():
                start -= 1

            start += 1
            end = root_index + 1

            if end < len(text) and text[end] == "(":
                end += 1
                number_start = end
                parentheses_count = 0

                while end < len(text):
                    if text[end] == "(":
                        parentheses_count += 1

                    elif text[end] == ")":
                        if parentheses_count == 0:
                            break

                        parentheses_count -= 1

                    end += 1

                number = text[number_start:end]

                if end < len(text) and text[end] == ")":
                    end += 1

            else:
                number_start = end

                while end < len(text) and (
                    text[end].isdigit()
                    or text[end] == "."
                ):
                    end += 1

                number = text[number_start:end]

            root_number = text[start:root_index]
            y = float(root_number)

            x = eval(
                prepare_expression(number)
            )

            if x < 0 and y % 2 == 0:
                result.config(text="Invalid input")
                return

            elif x < 0 and y % 2 != 0:
                value = -((-x) ** (1 / y))

                text = (
                    text[:start]
                    + str(value)
                    + text[end:]
                )
            else:
                value = x ** (1 / y)

                text = (
                    text[:start]
                    + str(value)
                    + text[end:]
                )

        # Handle percentages
        while "%" in text:
            percent_index = text.find("%")

            # Case 1: Percentage after a parenthesized expression
            # Example: (200+100)% → 3.0
            if percent_index > 0 and text[percent_index - 1] == ")":
                close_index = percent_index - 1
                count = 1
                start = close_index - 1

                while start >= 0:
                    if text[start] == ")":
                        count += 1

                    elif text[start] == "(":
                        count -= 1

                        if count == 0:
                            break

                    start -= 1

                if start < 0:
                    result.config(text="Invalid input")
                    return

                inside = text[start + 1:close_index]

                try:
                    number = eval(
                        prepare_expression(inside)
                    )
                except Exception:
                    result.config(text="Invalid input")
                    return

                value = number / 100

                text = (
                    text[:start]
                    + str(value)
                    + text[percent_index + 1:]
                )

                continue

            # Case 2: Find the number before %
            # Example: 50% → 0.5
            start = percent_index - 1

            while start >= 0 and (
                text[start].isdigit()
                or text[start] == "."
            ):
                start -= 1

            start += 1

            if start == percent_index:
                result.config(text="Invalid input")
                return

            try:
                number = float(
                    text[start:percent_index]
                )
            except ValueError:
                result.config(text="Invalid input")
                return

            # Case 3: Percentage at the beginning
            # Example: 50% → 0.5
            if start == 0:
                value = number / 100

                text = (
                    str(value)
                    + text[percent_index + 1:]
                )

                continue

            # Find the operator before the percentage number
            operator_index = start - 1
            operator = text[operator_index]

            # Case 4: Multiplication and division
            # Examples:
            # 200 × 10% → 200 × 0.1
            # 200 ÷ 10% → 200 ÷ 0.1
            if operator in ["x", "÷"]:
                value = number / 100

            # Case 5: Addition and subtraction
            # Examples:
            # 200 + 10% → 220
            # 200 - 10% → 180
            elif operator in ["+", "-"]:

                # If another multiplication or division operator
                # comes immediately after %, treat the percentage
                # as a normal decimal value.
                #
                # Example:
                # 200 + 10% × 5
                #
                # becomes:
                # 200 + 0.1 × 5
                if (
                    percent_index < len(text) - 1
                    and text[percent_index + 1] in ["x", "÷"]
                ):
                    value = number / 100

                else:
                    # Evaluate everything before the + or -
                    left_expression = text[:operator_index]

                    try:
                        left_value = eval(
                            prepare_expression(
                                left_expression
                            )
                        )
                    except Exception:
                        result.config(
                            text="Invalid input"
                        )
                        return

                    value = left_value * number / 100

            # Case 6: Any other situation
            # Treat the percentage as a normal decimal value
            else:
                value = number / 100

            # Replace number% with the calculated value
            text = (
                text[:start]
                + str(value)
                + text[percent_index + 1:]
            )

        # Process factorial expressions
        while "!" in text:
            index = text.find("!")

            if index > 0 and text[index - 1] == ")":
                close_index = index - 1
                count = 1
                start = close_index - 1

                while start >= 0:
                    if text[start] == ")":
                        count += 1

                    elif text[start] == "(":
                        count -= 1

                        if count == 0:
                            break

                    start -= 1

                if start < 0:
                    result.config(
                        text="Invalid input"
                    )
                    return

                number = text[start + 1:close_index]
                operand = prepare_expression(number)

                try:
                    value = eval(operand)
                except Exception:
                    result.config(
                        text="Invalid input"
                    )
                    return

                if not isinstance(value, (int, float)):
                    result.config(
                        text="Invalid input"
                    )
                    return

                if value < 0 or not float(value).is_integer():
                    result.config(
                        text="Invalid input"
                    )
                    return

                value = math.factorial(int(value))

                text = (
                    text[:start]
                    + str(value)
                    + text[index + 1:]
                )

            else:
                start = index - 1

                while start >= 0 and (
                    text[start].isdigit()
                    or text[start] == "."
                ):
                    start -= 1

                start += 1

                if start == index:
                    result.config(
                        text="Invalid input"
                    )
                    return

                # Prevent factorial from being applied to an invalid
                # negative number
                if start > 0 and text[start - 1] == "-":
                    if (
                        start - 1 == 0
                        or text[start - 2] in "+-x÷^("
                    ):
                        result.config(
                            text="Invalid input"
                        )
                        return

                number = text[start:index]

                try:
                    value = eval(number)
                except Exception:
                    result.config(
                        text="Invalid input"
                    )
                    return

                if not isinstance(value, (int, float)):
                    result.config(
                        text="Invalid input"
                    )
                    return

                if value < 0 or not float(value).is_integer():
                    result.config(
                        text="Invalid input"
                    )
                    return

                value = math.factorial(int(value))

                text = (
                    text[:start]
                    + str(value)
                    + text[index + 1:]
                )

        # Convert the final expression to Python syntax
        text = prepare_expression(text)

        # Evaluate the final expression
        answer = eval(text)

        # Add the calculation to history
        history.append(
            (original_expression, answer)
        )

        # Keep only the latest ten calculations
        if len(history) > 10:
            history.pop(0)

        result.config(text=answer)

        # Store the expression for repeated "=" behavior
        last_calculated_expression = expression.get()
        angle_mode_changed = False

    except:
        result.config(
            text="THERE IS AN ERROR IN YOUR EXPRESSION"
        )


# Add or close parentheses automatically
def add_parenthesis():
    text = expression.get()

    # Expression is empty → add an opening parenthesis
    if not text:
        expression.insert(tk.END, "(")
        return

    last_char = text[-1]

    open_count = text.count("(")
    close_count = text.count(")")
    unmatched = open_count - close_count

    # After an operator → add an opening parenthesis
    if last_char in operators:
        expression.insert(tk.END, "(")
        return

    # After an opening parenthesis
    if last_char == "(":
        # Do not allow more than two consecutive opening parentheses
        if text.endswith("(("):
            return

        expression.insert(tk.END, "(")
        return

    # After a number, decimal point, closing parenthesis, e, or π
    if (
        last_char.isdigit()
        or last_char == "."
        or last_char == ")"
        or last_char in ["e", "π"]
    ):
        # If there is an unmatched opening parenthesis → close it
        if unmatched > 0:
            expression.insert(tk.END, ")")

        else:
            # Otherwise → use implicit multiplication before opening
            # a new parenthesis
            expression.insert(tk.END, "x(")

        return


# Add a scientific function to the expression
def add_function(name):
    insert_with_multiplication(
        f"{name}("
    )


# Change the sign of the next value
def change_sign():
    text = expression.get()

    if not text:
        expression.insert(tk.END, "(-")
        return

    last_char = text[-1]

    # After an operator or opening parenthesis → insert (- 
    if last_char in operators or last_char == "(":
        expression.insert(tk.END, "(-")
        return

    # After a number, closing parenthesis, e, or π
    # → use implicit multiplication before the negative value
    if (
        last_char.isdigit()
        or last_char == ")"
        or last_char in ["e", "π"]
    ):
        expression.insert(tk.END, "x(-")
        return


# Insert the e^ function
def e():
    insert_with_multiplication("e^(")


# Square the entire expression
def expr2():
    text = expression.get()

    if not text:
        result.config(text="Invalid input")
        return

    # Automatically close unmatched parentheses
    while text.count("(") > text.count(")"):
        text += ")"

    new_text = f"({text})^(2)"

    expression.delete(0, tk.END)
    expression.insert(tk.END, new_text)


# Cube the entire expression
def expr3():
    text = expression.get()

    if not text:
        result.config(text="Invalid input")
        return

    # Automatically close unmatched parentheses
    while text.count("(") > text.count(")"):
        text += ")"

    new_text = f"({text})^(3)"

    expression.delete(0, tk.END)
    expression.insert(tk.END, new_text)


# Insert a custom power expression
def power_xy():
    text = expression.get()

    if not text:
        result.config(text="Invalid input")
        return

    end = len(text)

    # Find a numeric base
    if text[end - 1].isdigit() or text[end - 1] == ".":
        start = end - 1

        while start >= 0 and (
            text[start].isdigit()
            or text[start] == "."
        ):
            start -= 1

        start += 1

        # Include a valid negative sign in the base
        if start > 0 and text[start - 1] == "-" and (
            start - 1 == 0
            or text[start - 2] in "+-x÷("
        ):
            start -= 1

    # Find a parenthesized base
    elif text[end - 1] == ")":
        count = 0
        start = end - 1

        while start >= 0:
            if text[start] == ")":
                count += 1

            elif text[start] == "(":
                count -= 1

                if count == 0:
                    break

            start -= 1

        if start < 0:
            result.config(
                text="Invalid input"
            )
            return

    else:
        result.config(
            text="Invalid input"
        )
        return

    base = text[start:end]

    new_text = (
        text[:start]
        + f"({base})^("
    )

    expression.delete(0, tk.END)
    expression.insert(
        tk.END,
        new_text
    )


# Square the last part of the expression
def x2():
    text = expression.get()

    if not text:
        result.config(
            text="Invalid input"
        )
        return

    end = len(text)

    # Find a numeric value
    if text[end - 1].isdigit() or text[end - 1] == ".":
        start = end - 1

        while start >= 0 and (
            text[start].isdigit()
            or text[start] == "."
        ):
            start -= 1

        start += 1

        # Include a valid negative sign
        if start > 0 and text[start - 1] == "-" and (
            start - 1 == 0
            or text[start - 2] in "+-x÷("
        ):
            start -= 1

    # Find a parenthesized value
    elif text[end - 1] == ")":
        count = 0
        start = end - 1

        while start >= 0:
            if text[start] == ")":
                count += 1

            elif text[start] == "(":
                count -= 1

                if count == 0:
                    break

            start -= 1

        if start < 0:
            result.config(
                text="Invalid input"
            )
            return

    else:
        result.config(
            text="Invalid input"
        )
        return

    last_part = text[start:end]

    new_text = (
        text[:start]
        + f"({last_part})^(2)"
        + text[end:]
    )

    expression.delete(0, tk.END)
    expression.insert(
        tk.END,
        new_text
    )


# Cube the last part of the expression
def x3():
    text = expression.get()

    if not text:
        result.config(
            text="Invalid input"
        )
        return

    end = len(text)

    # Find a numeric value
    if text[end - 1].isdigit() or text[end - 1] == ".":
        start = end - 1

        while start >= 0 and (
            text[start].isdigit()
            or text[start] == "."
        ):
            start -= 1

        start += 1

        # Include a valid negative sign
        if start > 0 and text[start - 1] == "-" and (
            start - 1 == 0
            or text[start - 2] in "+-x÷("
        ):
            start -= 1

    # Find a parenthesized value
    elif text[end - 1] == ")":
        count = 0
        start = end - 1

        while start >= 0:
            if text[start] == ")":
                count += 1

            elif text[start] == "(":
                count -= 1

                if count == 0:
                    break

            start -= 1

        if start < 0:
            result.config(
                text="Invalid input"
            )
            return

    else:
        result.config(
            text="Invalid input"
        )
        return

    last_part = text[start:end]

    new_text = (
        text[:start]
        + f"({last_part})^(3)"
        + text[end:]
    )

    expression.delete(0, tk.END)
    expression.insert(
        tk.END,
        new_text
    )


# Insert 2^x
def power_2x():
    insert_with_multiplication("2^(")


# Insert scientific notation marker E
def exp():
    text = expression.get()

    if not text:
        result.config(
            text="Invalid input"
        )
        return

    expression.insert(
        tk.END,
        "E"
    )


# Insert the y√x expression
def root_xy():
    text = expression.get()

    if not text:
        result.config(
            text="invalid input"
        )
        return

    expression.insert(
        tk.END,
        "√("
    )


# Insert the reciprocal expression 1/x
def divide_by_x():
    expression.insert(
        tk.END,
        "1/("
    )


# Add factorial to the current value
def factorial():
    text = expression.get()

    if not text:
        result.config(
            text="Invalid input"
        )
        return

    if text[-1].isdigit() or text[-1] == ")":
        expression.insert(
            tk.END,
            "!"
        )


# Switch between DEG and RAD modes
def change_angle_mode():
    global angle_mode, angle_mode_changed

    if angle_mode == "DEG":
        angle_mode = "RAD"
    else:
        angle_mode = "DEG"

    angle_mode_changed = True

    # Always update the currently active angle button
    angle_button.config(
        text=angle_mode
    )


# Inverse mode state
inv_mode = False


# Switch between normal and inverse scientific functions
def change_inv_mode():
    global inv_mode, angle_button

    if inv_mode:
        normal_mode()
        return
    else:
        inv_mode = True

    # Remove the current scientific buttons
    for widget in scientific_frame.winfo_children():
        widget.destroy()

    # Buttons available in inverse mode
    inv_buttons = [
        ("Inv", 0, 0),
        ("DEG", 0, 1),
        ("³√", 0, 2),
        ("2ˣ", 0, 3),
        ("sin⁻¹", 1, 0),
        ("cos⁻¹", 1, 1),
        ("tan⁻¹", 1, 2),
        ("cot⁻¹", 1, 3),
        ("sinh", 2, 0),
        ("cosh", 2, 1),
        ("tanh", 2, 2),
        ("coth", 2, 3),
        ("sinh⁻¹", 3, 0),
        ("cosh⁻¹", 3, 1),
        ("tanh⁻¹", 3, 2),
        ("coth⁻¹", 3, 3),
        ("(Expr)³", 4, 0),
        ("x³", 4, 1),
        ("Exp", 4, 2),
        ("+/-", 4, 3)
    ]

    if inv_mode:
        buttons = inv_buttons
    else:
        buttons = normal_buttons

    # Create the inverse-mode buttons
    for text, row, col in buttons:
        original_text = text

        # Display the current angle mode
        if text == "DEG":
            text = angle_mode

        # Connect scientific function buttons to add_function()
        if original_text in [
            "³√",
            "sin⁻¹",
            "cos⁻¹",
            "tan⁻¹",
            "sinh",
            "cosh",
            "tanh",
            "sinh⁻¹",
            "cosh⁻¹",
            "tanh⁻¹",
            "²√",
            "sin",
            "cos",
            "tan",
            "cot",
            "log",
            "ln"
        ]:
            command = lambda x=original_text: add_function(x)

        elif original_text == "DEG":
            command = change_angle_mode

        elif original_text == "Inv":
            command = change_inv_mode

        elif original_text == "+/-":
            command = change_sign

        elif original_text == "cot⁻¹":
            command = lambda: add_function("cot⁻¹")

        elif original_text == "coth":
            command = lambda: add_function("coth")

        elif original_text == "coth⁻¹":
            command = lambda: add_function("coth⁻¹")

        elif original_text == "(Expr)³":
            command = expr3

        elif original_text == "x³":
            command = x3

        elif original_text == "2ˣ":
            command = power_2x

        elif original_text == "Exp":
            command = exp

        else:
            command = lambda x=original_text: add_to_expression(x)

        # Create the scientific button
        button = tk.Button(
            scientific_frame,
            text=text,
            font=("georgia", 14),
            bg="black",
            fg="white",
            borderwidth=10,
            command=command
        )

        # Store a reference to the angle-mode button
        if original_text == "DEG":
            angle_button = button

        button.grid(
            row=row,
            column=col,
            sticky="nsew",
            padx=3,
            pady=3
        )


# Restore the normal scientific button layout
def normal_mode():
    # This function only restores the Scientific buttons.
    # It does not change the main window row sizes.
    #
    # When Scientific mode is visible:
    # Display = 85%
    # Scientific = 5%
    # Main = 10%
    #
    # When Scientific mode is hidden:
    # toggle_scientific() controls the row sizes:
    # Display = 45%
    # Scientific = 0%
    # Main = 55%

    global inv_mode, angle_button

    inv_mode = False

    # Remove the current scientific buttons
    for widget in scientific_frame.winfo_children():
        widget.destroy()

    # Create the normal scientific buttons
    for text, row, col in normal_buttons:

        if text in [
            "²√",
            "sin",
            "cos",
            "tan",
            "cot",
            "log",
            "ln"
        ]:
            command = lambda x=text: add_function(x)

        elif text == "|x|":
            command = lambda: add_function("abs")

        elif text == "+/-":
            command = change_sign

        elif text == "eˣ":
            command = e

        elif text == "(Expr)²":
            command = expr2

        elif text == "xʸ":
            command = power_xy

        elif text == "x²":
            command = x2

        elif text == "y√x":
            command = root_xy

        elif text == "DEG":
            command = change_angle_mode

        elif text == "Inv":
            command = change_inv_mode

        elif text == "1/x":
            command = divide_by_x

        elif text == "x!":
            command = factorial

        else:
            command = lambda x=text: add_to_expression(x)

        # Create the scientific button
        button = tk.Button(
            scientific_frame,
            text=(
                angle_mode
                if text == "DEG"
                else text
            ),
            font=("georgia", 14),
            bg="black",
            fg="white",
            borderwidth=10,
            command=command
        )

        # Store a reference to the angle-mode button
        if text == "DEG":
            angle_button = button

        button.grid(
            row=row,
            column=col,
            sticky="nsew",
            padx=3,
            pady=3
        )


# Show or hide the Scientific section
def toggle_scientific():
    global scientific_visible

    if scientific_visible:
        # Scientific section is hidden
        scientific_frame.grid_remove()

        # Scientific row should take no extra space.
        # Display = 45%
        # Scientific = 0%
        # Main = 55%
        window.grid_rowconfigure(
            0,
            weight=45,
            minsize=0
        )

        window.grid_rowconfigure(
            1,
            weight=0,
            minsize=0
        )

        window.grid_rowconfigure(
            2,
            weight=55,
            minsize=0
        )

        scientific_visible = False

    else:
        # Scientific section is visible
        scientific_frame.grid(
            row=1,
            column=0,
            columnspan=4,
            sticky="nsew"
        )

        # Display = 85%
        # Scientific = 5%
        # Main = 10%
        window.grid_rowconfigure(
            0,
            weight=85,
            minsize=0
        )

        window.grid_rowconfigure(
            1,
            weight=5,
            minsize=0
        )

        window.grid_rowconfigure(
            2,
            weight=10,
            minsize=0
        )

        scientific_visible = True


# Show or hide the calculation history
def show_history():
    global history_frame

    # Close the history panel if it is already open
    if history_frame is not None:
        history_frame.destroy()
        history_frame = None
        return

    # Create the history panel
    history_frame = tk.Frame(
        window,
        bg="white",
        width=300,
        height=350
    )

    history_frame.place(
        relx=1.0,
        x=-10,
        y=70,
        anchor="ne"
    )

    history_frame.pack_propagate(False)

    # Create the history text area
    history_text = tk.Text(
        history_frame,
        bg="white",
        fg="black",
        font=("Consolas", 18),
        relief=tk.FLAT,
        borderwidth=0
    )

    # Create the scrollbar
    scrollbar = tk.Scrollbar(
        history_frame,
        orient="vertical",
        width=18,
        command=history_text.yview
    )

    # Pack the scrollbar first
    scrollbar.pack(
        side="right",
        fill="y"
    )

    # Then pack the text area
    history_text.pack(
        side="left",
        fill="both",
        expand=True
    )

    # Connect the Text widget to the scrollbar
    history_text.configure(
        yscrollcommand=scrollbar.set
    )

    # Display calculation history
    for expr, answer in history:
        history_text.insert(
            tk.END,
            expr + "\n"
        )

        history_text.insert(
            tk.END,
            "result = " + str(answer) + "\n\n"
        )

    # Make the history text read-only
    history_text.config(
        state="disabled"
    )


# Configure the main window columns
window.grid_columnconfigure(
    0,
    weight=1
)

window.grid_columnconfigure(
    1,
    weight=1
)

window.grid_columnconfigure(
    2,
    weight=1
)

# Configure the initial window rows
window.grid_rowconfigure(
    0,
    weight=45,
    minsize=0
)

window.grid_rowconfigure(
    1,
    weight=0,
    minsize=0
)

window.grid_rowconfigure(
    2,
    weight=55,
    minsize=0
)


# Create the display frame
display_frame = tk.Frame(
    window,
    bg="black"
)

display_frame.grid(
    row=0,
    column=0,
    columnspan=4,
    sticky="nsew"
)


# History and Scientific/Phone buttons are placed inside
# the same frame so their distance does not grow with the window.
# Both buttons remain together in the upper-right corner.
top_buttons_frame = tk.Frame(
    window,
    bg="black"
)

top_buttons_frame.place(
    relx=1.0,
    rely=0.01,
    anchor="ne"
)


# Create the history button
history_button = tk.Button(
    top_buttons_frame,
    text="◷",
    command=show_history,
    bg="black",
    fg="white",
    borderwidth=0,
    font=("georgia", 22)
)

history_button.pack(
    side="left",
    padx=(0, 4)
)


# Create the Scientific/Phone layout button
size_button = tk.Button(
    top_buttons_frame,
    text="📱",
    command=toggle_scientific,
    bg="black",
    fg="white",
    borderwidth=0,
    font=("georgia", 22)
)

size_button.pack(
    side="left",
    padx=(0, 0)
)


# Create the expression input field
expression = tk.Entry(
    display_frame,
    font=("consolas", 24),
    bg="black",
    fg="white",
    relief=tk.FLAT,
    borderwidth=0
)

expression.grid(
    row=0,
    column=0,
    columnspan=4,
    sticky="nsew"
)


# Create the result display
result = tk.Label(
    display_frame,
    text="",
    font=("consolas", 24),
    bg="black",
    fg="white",
    anchor="w",
    relief=tk.FLAT,
    borderwidth=0
)

result.grid(
    row=1,
    column=0,
    columnspan=4,
    sticky="nsew"
)


# Configure the display columns
for i in range(4):
    display_frame.grid_columnconfigure(
        i,
        weight=1
    )


# Configure the display rows
display_frame.grid_rowconfigure(
    0,
    weight=60
)

display_frame.grid_rowconfigure(
    1,
    weight=40
)


# Create the Scientific section
scientific_frame = tk.Frame(
    window,
    bg="black"
)

scientific_frame.grid(
    row=1,
    column=0,
    columnspan=4,
    sticky="nsew"
)


# Configure Scientific section columns
for i in range(4):
    scientific_frame.grid_columnconfigure(
        i,
        weight=1,
        uniform="col"
    )


# Configure Scientific section rows
for i in range(5):
    scientific_frame.grid_rowconfigure(
        i,
        weight=1
    )


# Normal scientific calculator buttons
normal_buttons = [
    ("Inv", 0, 0),
    ("DEG", 0, 1),
    ("²√", 0, 2),
    ("|x|", 0, 3),
    ("sin", 1, 0),
    ("cos", 1, 1),
    ("tan", 1, 2),
    ("cot", 1, 3),
    ("ln", 2, 0),
    ("log", 2, 1),
    ("1/x", 2, 2),
    ("e", 2, 3),
    ("eˣ", 3, 0),
    ("x²", 3, 1),
    ("xʸ", 3, 2),
    ("π", 3, 3),
    ("(Expr)²", 4, 0),
    ("x!", 4, 1),
    ("y√x", 4, 2),
    ("+/-", 4, 3)
]


# Initialize the Scientific section in normal mode
normal_mode()

# Hide the Scientific section when the calculator starts
scientific_frame.grid_remove()

# Restore the initial window row configuration
window.grid_rowconfigure(
    0,
    weight=45,
    minsize=0
)

window.grid_rowconfigure(
    1,
    weight=0,
    minsize=0
)

window.grid_rowconfigure(
    2,
    weight=55,
    minsize=0
)


# Create the main calculator button frame
main_button_frame = tk.Frame(
    window,
    bg="black"
)

main_button_frame.grid(
    row=2,
    column=0,
    columnspan=4,
    sticky="nsew"
)


# Configure main button columns
for i in range(4):
    main_button_frame.grid_columnconfigure(
        i,
        weight=1,
        uniform="col"
    )


# Configure main button rows
for i in range(5):
    main_button_frame.grid_rowconfigure(
        i,
        weight=1
    )


# Main calculator buttons
main_buttons = [
    ("C", 0, 0),
    ("Del", 0, 1),
    ("%", 0, 2),
    ("÷", 0, 3),
    ("7", 1, 0),
    ("8", 1, 1),
    ("9", 1, 2),
    ("x", 1, 3),
    ("4", 2, 0),
    ("5", 2, 1),
    ("6", 2, 2),
    ("-", 2, 3),
    ("1", 3, 0),
    ("2", 3, 1),
    ("3", 3, 2),
    ("+", 3, 3),
    ("()", 4, 0),
    ("0", 4, 1),
    (".", 4, 2),
    ("=", 4, 3)
]


# Create all main calculator buttons
for text, row, col in main_buttons:

    if text == "C":
        command = clear

    elif text == "Del":
        command = Delete

    elif text == "=":
        command = calculate

    elif text == "()":
        command = add_parenthesis

    else:
        command = lambda x=text: add_to_expression(x)

    button = tk.Button(
        main_button_frame,
        text=text,
        font=("georgia", 18),
        bg="black",
        fg="white",
        borderwidth=10,
        command=command
    )

    button.grid(
        row=row,
        column=col,
        sticky="nsew",
        padx=3,
        pady=3 
    )


# Start the Tkinter event loop
window.mainloop()