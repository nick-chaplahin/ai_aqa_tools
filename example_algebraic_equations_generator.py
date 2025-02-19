"""
Examples of Complex equations generator usage
Author: Nick  Chaplahin, 2025
Copyright: Nick Chaplahin

License: MIT

"""
from algebraic_equations_generator import AlgebraicEquationGenerator
import sympy

equation = AlgebraicEquationGenerator()

print (f"\n\n============================== EQUATION DEFAULT ==============================================")
equation.generate_equation()
init_equation = equation.get_init_expression()
print(f"Solution/initial equation: {init_equation[0]} = {init_equation[1]}")
print(f"LaTeX Solution/initial equation: {sympy.latex(sympy.simplify(init_equation[0]))} = \
{sympy.latex(sympy.simplify(init_equation[1]))}")
print(f"Positive: {equation.get_result()[0]}, Result: {equation.get_result()[1]}")
equation_math = equation.get_equation()
print("Complicated Equation: {} = {}".format(equation_math[0], equation_math[1]))
print("LaTeX Complicated Equation: {} = {}".format(sympy.latex(equation_math[0]), sympy.latex(equation_math[1])))
print(f"Description of equation: {equation.get_string_equation()[0]} equals to {equation.get_string_equation()[1]}")
print("Solution path:")
solution_path = equation.get_resolve_path()
for line in solution_path:
    print(line)

print(f"\n\n============================== EQUATIONS UPDATED ==============================================")
equation.set_expression_length((3, 3))
equation.set_complication_depth((3, 3))
equation.set_symbols_density(0.7)
operation_text_operands = {
    'add': ['add', 'plus', '+'],
    'sub': ['sub', 'minus', '-'],
    'multiply': ['multiply by', 'mul', '*', 'x'],
    'divide': ['divide by', 'div', ':', '/'],
    'power': [' power to ', '^', '**'],
}
equation.set_operation_operands(operation_text_operands)
for _ in range(20):
    equation.generate_equation()
    init_equation = equation.get_init_expression()
    print(f"Solution/initial equation: {init_equation[0]} = {init_equation[1]}")
    print(f"Equation: {equation.get_equation()[0]} = {equation.get_equation()[1]}")
    print(f"Description of equation: {equation.get_string_equation()[0]} = {equation.get_string_equation()[1]}")
    print("\n")
