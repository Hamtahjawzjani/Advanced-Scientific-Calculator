# 🧮 Advanced Scientific Calculator

A feature-rich **Advanced Scientific Calculator** built with **Python and Tkinter**, designed to provide a clean, responsive, and practical calculator experience with both basic and advanced mathematical operations.

The calculator combines standard arithmetic operations with a wide range of scientific functions, angle modes, inverse functions, expression-based calculations, calculation history, percentage operations, and more.

---

## ✨ Features

### 🔢 Basic Calculator

Supports all essential arithmetic operations:

* Addition `+`
* Subtraction `−`
* Multiplication `×`
* Division `÷`
* Percentage `%`
* Sign change `+/−`
* Decimal numbers
* Delete and Clear operations
* Automatic multiplication where appropriate
* Error handling for invalid expressions

---

## 🔬 Scientific Calculator

The scientific mode provides a wide range of advanced mathematical functions.

### 📐 Trigonometric Functions

* `sin`
* `cos`
* `tan`
* `cot`

### 🔄 Inverse Trigonometric Functions

* `sin⁻¹`
* `cos⁻¹`
* `tan⁻¹`
* `cot⁻¹`

### 📊 Hyperbolic Functions

* `sinh`
* `cosh`
* `tanh`
* `coth`

### 🔄 Inverse Hyperbolic Functions

* `sinh⁻¹`
* `cosh⁻¹`
* `tanh⁻¹`
* `coth⁻¹`

---

# ⭐ Advanced Features

One of the main goals of this calculator is to provide functionality that is often missing from the standard calculator applications found on phones.

## 🔥 Extended Cotangent Functions

Unlike many standard mobile calculators, this calculator provides a complete set of **cotangent-related functions**:

* **`cot` — Cotangent**
* **`cot⁻¹` — Inverse Cotangent**
* **`coth` — Hyperbolic Cotangent**
* **`coth⁻¹` — Inverse Hyperbolic Cotangent**

These functions are directly available through the scientific interface, making the calculator more useful for advanced mathematical calculations.

---

## 🧠 Expression Power Functions

The calculator supports raising an entire mathematical expression to a power.

### **`(Expr)²`**

Allows the user to calculate the square of a complete expression.

For example:

`(2 + 3)²`

### **`(Expr)³`**

Allows the user to calculate the cube of a complete expression.

For example:

`(2 + 3)³`

This makes it possible to work with complete expressions instead of manually calculating intermediate results.

---

## √ Custom Root — `y√x`

The calculator supports **roots with a user-defined index**, allowing calculations beyond the standard square root and cube root.

For example:

`3√27 = 3`

The user can choose the root index instead of being limited to only:

* `√x`
* `³√x`

This provides greater flexibility for mathematical and scientific calculations.

---

## ⚡ `eˣ`, `2ˣ` and Exponential Calculations

The calculator supports exponential calculations using:

* `eˣ`
* `2ˣ`
* `xʸ`

It also supports the mathematical constant:

### **`e`**

where:

`e ≈ 2.718281828...`

---

## π — Pi Constant

The calculator includes the **π (Pi)** constant for mathematical and trigonometric calculations.

`π ≈ 3.141592653...`

Pi can be used directly inside expressions without manually entering its numerical value.

---

## 🔬 Scientific Notation — `Exp`

The calculator also includes an **`Exp`** button for entering numbers using scientific notation.

For example:

`5 Exp 3`

represents:

`5 × 10³`

This is particularly useful when working with very large or very small numbers.

---

# 📐 DEG / RAD Modes

The calculator supports two angle modes:

* **DEG** — Degrees
* **RAD** — Radians

The selected mode is applied to trigonometric calculations such as:

`sin`, `cos`, `tan`, and `cot`

The angle mode can be switched directly using the **DEG/RAD** button.

---

# 🔄 Inverse Mode

The **Inv** button switches the scientific keypad between normal and inverse functions.

This provides access to additional mathematical operations without making the interface unnecessarily crowded.

---

# 📚 Additional Scientific Functions

The calculator also supports:

### Logarithmic Functions

* `log`
* `ln`

### Roots

* `√x`
* `³√x`
* `y√x`

### Powers

* `x²`
* `x³`
* `xʸ`
* `eˣ`
* `2ˣ`
* `(Expr)²`
* `(Expr)³`

### Other Functions

* `|x|`
* `1/x`
* Factorial `!`
* `+/−`
* `e`
* `π`

---

# 🕘 Calculation History

The calculator includes a **History** feature that keeps track of recent calculations.

This allows users to review previous expressions and their results without having to calculate them again.

The history is designed to remain concise by keeping the most recent calculations.

---

# 🛡️ Error Handling

The calculator includes error handling for invalid or unsupported mathematical expressions.

Instead of allowing the application to crash, invalid calculations are handled gracefully and an appropriate error result is displayed.

---

# 🖥️ Screenshots

## Basic Calculator

<!-- Add screenshot here -->

## Scientific Mode

<!-- Add screenshot here -->

## Inverse Mode

<!-- Add screenshot here -->

## Calculation History

<!-- Add screenshot here -->

---

# 🛠️ Technologies

This project was built using:

* **Python**
* **Tkinter**
* **Math**
* **Regular Expressions (`re`)**

Tkinter is used to create the graphical user interface, while Python's mathematical capabilities are used to perform scientific calculations.

---

# 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/Advanced-Scientific-calculator.git
```

### 2. Open the project directory

```bash
cd Advanced-Scientific-calculator
```

### 3. Run the calculator

```bash
python "Advanced-Scientific calculator.py"
```

> Make sure Python is installed on your system.

---

# 📦 Windows Executable

A standalone **Windows `.exe` version** of the calculator is also provided through the project's GitHub Releases.

The executable allows Windows users to run the calculator without manually running the Python source code.

**Download the latest Windows version from the Releases section.**

---

# 📂 Project Structure

```text
scientific-calculator/
│
├── scientific calculator.py
├── README.md
├── .gitignore
└── screenshots/
    ├── basic.png
    ├── scientific.png
    ├── inverse.png
    └── history.png
```

---

# 🎯 Project Goals

The goal of this project is to create a practical scientific calculator that combines:

* A clean graphical interface
* Standard calculator functionality
* Advanced scientific operations
* Flexible expression handling
* Multiple angle modes
* Inverse and hyperbolic functions
* Calculation history
* Error handling
* A standalone Windows executable

The project also serves as a practical demonstration of building a complete GUI application using Python and Tkinter.

---

# 👨‍💻 Author

**Hamtah Jawzjani**

Built with Python 🐍 and Tkinter 🖥️

---

## 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for more information.

