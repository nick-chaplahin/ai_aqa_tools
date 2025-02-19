Automatic algebraic equations generator.

Generator of complex equations. 
Like, 
   Solution/initial equation: 84.04502*x - 57.36038*y + 59 = 0
   Complex Equation: 2*x**2 + x + zoo*(84.04502*x - 57.36038*y + 59) - (1/x)**x = nan
   Description of complex equation: (0 + 84.04502 mul x add -57.36038 multiply by y add 59) / (((x - x) / x) ** 199) minus (((x : x) : x)  power to  x) add ((x plus x) mul x add x) = 0  / (((x - x) / x) ** 199) minus (((x : x) : x)  power to  x) add ((x plus x) mul x add x)

Generates:
1. In Positive scenario:
   - complex algebraic equation with symbolic variables, 
   - initial expression (as a solution for complex equation "simplify" task
   - roots of the initial expression (as a solution for initial equation, if available)
   - textual description of the equation, where + - / can be replaced by "add", "sub", "divide by" and so on.
   - List of resolution steps - list of actions that should be done to simplify complex equations to initial form.
   - Also, users can get the LaTeX format of the complex and initial equations.

2. In Negative scenario:
   - Textual description of the equation, where + - / can be replaced by "add", "sub", "divide by" and so on.
   - Expected error type.
Note: complex equation, result of equation are 0-s in this case, because they are not computable due to error.

Requirements:
   sympy

Issues:
   - sympy.solve can hang time-to-time with very complex equations. For a start - try smaller ranges and complication depth.
   - sympy.latex for "general" types of equations can crash if a fraction is in params. To display LaTeX representation of the equation use sympy.latex(sympy.simplify(equation)). See example_algebraic_equation_generator for working examples.

Recommended:
   - If you can replace the sympy module by one you use  - do it.
   - For simpler tasks use smaller ranges of values and less depth of the equation complication.
