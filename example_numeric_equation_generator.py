"""
Examples of Complex equations generator usage
Author: Nick  Chaplahin, 2025
Copyright: Nick Chaplahin

License: MIT

"""

from numeric_equations_generator import EquationGenerator

# Create a class
equation = EquationGenerator()
# Setup number of values to be used in the equation
equation.set_values_num((10, 15))

# Generate equations
for idx in range(5):
    equation.generate_equation()
    print("Equation: {}".format(equation.get_equation()))
    print("LaTeX Equation: {}".format(equation.get_latex_equation()))
    result = equation.get_result()
    print(" Positive_Test: {} \n Result: {} \n ExpectedErrorType: {}".format(result[0], result[1], result[2]))

# Redefine parameters of the equation generator
operation_text_operands = {
    'add': ['add', 'plus', '+'],
    'sub': ['sub', 'minus', '-'],
    'multiply': ['multiply by', 'mul', '*', 'x'],
    'divide': ['divide by', 'div', ':', '/'],
    'power': [' power to ', '^', '**'],
    'logarithm': ['logarithm of ({}) base ({})', 'log({},{})', 'log_({}) ({})', 'logarithm ({}) base ({})'],
    'euler_num': ['{} multiply by e power to ({})', '{} mul e^({})', '{} * e^({})', '{} mul by e ** ({})']
}
equation.set_operation_operands(operation_text_operands)

# Generate new equations
for idx in range(5):
    equation.generate_equation()
    print("Equation for Eval : {}".format(equation.get_eval_equation()))
    print("Equation: {}".format(equation.get_equation()))
    print("LaTeX Equation: {}".format(equation.get_latex_equation()))
    result = equation.get_result()
    print(" Positive_Test: {} \n Result: {} \n ExpectedErrorType: {}".format(result[0], result[1], result[2]))
