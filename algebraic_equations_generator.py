"""
Automatic complex algebraic equations generator
Author: Nick  Chaplahin, 2025
Copyright: Nick Chaplahin

License: MIT

IMPORTANT: Sympy is required:
pip install sympy

Class AlgebraicEquationGenerator generates algebraic equations with symbolic variables (x, y, a-b-c, configurable).
To generate a complex equation script generates initial expression of defined type and length. User can define initial
expression using Sympy expression, and string description of this expression.
         expression
    left {side} = right {side}
or, that is the same
     left {side} - right {side} = 0

All expression are in format of tuple (left, right).
Script generates both sympy expression and string representation of the equation, using self.operation_operands for text
representation of the expression.
 so final equation will be
     left(sympy), right(sympy)
     left(string), right(string)

Process of Complex equation generation briefly:
1. Generate initial expression.
    1.a. Simplified (SYMPY.SIMPLIFY) initial equation is a solution for "simplify" tasks.
    1.b. Roots of initial equation (SYMPY.SOLVE) are expected answers for "resolve" tasks.
2. Generate expression as "extension" for the equation complication, and action
3. Complicate equation by
    left {action} expression, right {action} expression
    For example:
    1. Initial expression     (sympy):  x+3, 0,              (string): 'x add 3', 'nothing'
    2. Expression to extend   (sympy):  x*2                  (string): 'x multiply by 2'
    3. Action to extend       (sympy):  /                    (string): 'divide by'
    3. Complicated expression (sympy):  (x+3)/(x*2), 0/(x*2) (string): '(x add 3) divide by (x multiply by 2',
                                                                                  'nothing divide by (x multiply by 2)'

"""

import sympy
import fractions
import random


class AlgebraicEquationGenerator:

    def __init__(self):
        # Configuration parameters
        self.equation_type = "linear"
        self.supported_equation_types = ["linear", "quadratic", "cubic", "general"]
        self.expression_length = (1, 5)
        self.complication_depth = (2, 5)
        self.type_probabilities = [0.4, 0.2, 0.4]  # [integer, float, fraction]
        self.type_ranges = {
            "integer": (-100, 200),
            "float": (-100.0, 200.0),
            "fraction": ((-100, 200), (-400, 400)),
        }
        self.operation_probabilities = {
            'add': 0.25,
            'sub': 0.25,
            'multiply': 0.15,
            'divide': 0.15,
            'power': 0.1
        }
        self.operation_operands = {
            'add': '+',
            'sub': '-',
            'multiply': '*',
            'divide': '/',
            'power': ' ** '
        }
        self.symbol_probabilities = {
            sympy.Symbol("x"): 0.8,
            sympy.Symbol("y"): 0.2
        }
        self.symbols_density = 0.3  # probability of selecting symbol for complication expression
        self.init_expression = ""  # initial equation, configurable
        self.init_expression_str = ""
        self.positive_flag = True
        self.result = 0  # result of equation
        self.error_type = ""
        self.resolving_path = []
        self.equation = 0
        self.equation_str = ""
        self.log_level = 1

    def _service_log(self, text, module, level):
        """
        Procedure to print logs. Print logs which level is <=  configured self.log_level.
           Accepted levels are 1-5, where 1 - exception, 5 - info about selected value.
           Use self.log_level to no print logs
        :param text: Log information
        :param module: From which procedure log is. Word '_service' is omitted in modules
        :param level: Level of the issue (1-5)
        :return:
        none
        """
        if level <= self.log_level:
            print(f"[LOG_MESSAGE] [Level {level}] [IN {module}] {text}")

    def _service_get_rnd_type(self):
        """
        According to self.type_probabilities 'randomly' selects variable type.
        :return:
        - type as String
        """
        types = list(self.type_ranges.keys())
        generated_type = random.choices(types, weights=self.type_probabilities)[0]
        self._service_log(f"Type generated: {generated_type}", "get_rnd_type", 5)
        return generated_type

    def _service_generate_symbol(self):
        """
        According to self.symbol_probabilities 'randomly' selects sympy.Symbol to use in expression.
        :return:
        - selected symbol as sympy.Symbol
        - selected symbol as String
        """
        symbol_values = list(self.symbol_probabilities.keys())
        symbol_weights = list(self.symbol_probabilities.values())
        symbol_val = random.choices(symbol_values, weights=symbol_weights)[0]
        self._service_log(f"Symbol generated: {symbol_val}", "generate_symbol", 5)
        return symbol_val, str(symbol_val)

    def _service_not_val_or_symbol(self, value):
        """
        Procedure to check if value is int, float, fraction or Symbol. If not - return True, else - False
        :param value: Variable to check
        :return:
        """
        if isinstance(value, int):
            return False
        if isinstance(value, float):
            return False
        if isinstance(value, fractions.Fraction):
            return False
        if isinstance(value, sympy.Symbol):
            return False
        return True

    def _service_generate_value(self, value_type=""):
        """
        According to self.type_probabilities selects value of variable type. Then generates a 'random' value
            withing configured boundaries for a type self.type_ranges.
        :return:
        - numerical representation of the value, for fractions in fractions.Fraction type
        - string representation of the value,
        """
        if not value_type:
            value_type = self._service_get_rnd_type()
        if value_type == "integer":
            num = random.randint(self.type_ranges["integer"][0], self.type_ranges["integer"][1])
            while num == 0:
                num = random.randint(self.type_ranges["integer"][0], self.type_ranges["integer"][1])
            self._service_log(f"Int generated: {num}", "generate_value", 5)
            return num, str(num)
        elif value_type == 'float':
            num = round(random.uniform(self.type_ranges["float"][0], self.type_ranges["float"][1]), 5)
            while num == 0.0:
                num = round(random.uniform(self.type_ranges["float"][0], self.type_ranges["float"][1]), 5)
            self._service_log(f"Float generated: {'%.5f' % num}", "generate_value", 5)
            return float("%.5f" % num), str(float("%.5f" % num))
        elif value_type == 'fraction':  # fraction
            numerator = random.randint(self.type_ranges["fraction"][0][0], self.type_ranges["fraction"][0][1])
            while numerator == 0:
                numerator = random.randint(self.type_ranges["fraction"][0][0], self.type_ranges["fraction"][0][1])
            denominator = random.randint(self.type_ranges["fraction"][1][0], self.type_ranges["fraction"][1][1])
            while denominator == 0:
                denominator = random.randint(self.type_ranges["fraction"][1][0], self.type_ranges["fraction"][1][1])
            num = fractions.Fraction(numerator, denominator)
            str_val = f"({num.numerator}/{num.denominator})"
            self._service_log(f"Fraction generated: {str_val}", "generate_value", 5)
            return num, str_val

    def _service_get_symbol_or_value(self):
        """
        According to self.symbols_density 'randomly' generates either symbol or a value for expression.
        :return:
        - symbol as sympy.Symbol or value as int or float or Fraction
        """
        if random.random() < self.symbols_density:
            return self._service_generate_symbol()
        else:
            return self._service_generate_value()

    def _service_get_operation_description(self, action):
        """
        Procedure for selection of text representation of operation action from self.operation_operands for text
            representation of expression.
        :param action: action from list of supported actions
        :return:
        - 'randomly' selected operation description from self.operation_operands if it is a list, or actual
            operation description if only one value available.
        """
        if isinstance(self.operation_operands[action], list):
            generated_operation_description = random.choice(self.operation_operands[action])
            self._service_log(f"Generated operation: {generated_operation_description}", "get_operation_description", 5)
            return generated_operation_description
        else:
            self._service_log(f"Returned operation: {self.operation_operands[action]}", "get_operation_description", 5)
            return self.operation_operands[action]

    def _service_apply_action(self, left_operand, right_operand, left_str, right_str, action):
        """
        Procedure to generate a part of equation around single operator. Each operation schematically can be
            represented as '{} action {}'. So left is left operand (value or part of equation), right is right operand
            (value or part of the equation), and action is an operator.
        Note: can be specific cases like exponent and logarithm.
            exponent is e^{}, to simplify code it is being build as {left} * e^{right}. TBD - add dynamic selection of
            operand instead of '*'
            logarithm is log({value}, {base}), where {base} = {left} and {value} = {right}

        :param left_operand: left operand for action
        :param right_operand: right operand for action
         param left_str: String representation of left operand
        :param right_str: String representation of right operand
        :param action: math operation
        :return:
        - Ready-for-Python-sympy-expression of {left operand} {action} {right operand} in python sympy format.
        - String of text representation of operation description where action is replaced by 'random'
            'self.operation_operands' for this action
        """
        action_description = self._service_get_operation_description(action)
        if action == 'add':
            expression = 0
            if self.positive_flag:
                try:
                    expression = left_operand + right_operand
                except OverflowError:
                    self.positive_flag = False
                    self.result = 0
                    self.error_type = "OverflowError"
                    self._service_log(f"Applied action: {action}, get OverflowError", "apply_action", 1)
            self._service_log(f"Applied action: {action}, get expression: {expression }", "apply_action", 4)
            return expression, f"{left_str} {action_description} {right_str}"
        elif action == 'sub':
            expression = 0
            if self.positive_flag:
                try:
                    expression = left_operand - right_operand
                except OverflowError:
                    self.positive_flag = False
                    self.result = 0
                    self.error_type = "OverflowError"
                    self._service_log(f"Applied action: {action}, get OverflowError", "apply_action", 1)
            self._service_log(f"Applied action: {action}, get expression: {expression}", "apply_action", 4)
            return expression, f"{left_str} {action_description} {right_str}"
        elif action == 'multiply':
            expression = 0
            if self._service_not_val_or_symbol(left_operand):
                left_str = f"({left_str})"
            if self._service_not_val_or_symbol(right_operand):
                right_str = f"({right_str})"
            if self.positive_flag:
                try:
                    expression = left_operand * right_operand
                except OverflowError:
                    self.positive_flag = False
                    self.result = 0
                    self.error_type = "OverflowError"
                    self._service_log(f"Applied action: {action}, get OverflowError", "apply_action", 1)
            self._service_log(f"Applied action: {action}, get expression: {expression}", "apply_action", 4)
            return expression, f"{left_str} {action_description} {right_str}"
        elif action == 'divide':
            expression = 0
            if self._service_not_val_or_symbol(left_operand):
                left_str = f"({left_str})"
            if self._service_not_val_or_symbol(right_operand):
                right_str = f"({right_str})"
            if self.positive_flag:
                try:
                    expression = left_operand / right_operand
                except OverflowError:
                    self.positive_flag = False
                    self.result = 0
                    self.error_type = "OverflowError"
                    self._service_log(f"Applied action: {action}, got OverflowError", "apply_action", 1)
            self._service_log(f"Applied action: {action}, got expression: {expression}", "apply_action", 4)
            return expression, f"{left_str} {action_description} {right_str}"
        elif action == 'power':
            expression = 0
            if self._service_not_val_or_symbol(left_operand):
                left_str = f"({left_str})"
            if self._service_not_val_or_symbol(right_operand):
                right_str = f"({right_str})"
            if self.positive_flag:
                try:
                    expression = left_operand ** right_operand
                    self._service_log(f"Applied action: {action}, got expression: {expression}", "apply_action", 4)
                except OverflowError:
                    self.positive_flag = False
                    self.result = 0
                    self.error_type = "OverflowError"
                    self._service_log(f"Applied action: {action}, got OverflowError", "apply_action", 1)
            return expression, f"{left_str} {action_description} {right_str}"
        """
        <TBD> -  add support of logarithms and euler num
        elif action == 'logarithm':
            expression = sympy.log(left_operand, right_operand)
            self._service_log(f"Applied action: {action}, got expression: {expression}", "apply_action", 4)
            return expression, f"{action_description}({left_str}, {right_str})"
        elif action == 'euler_num':
            expression = left_operand * sympy.euler(right_operand)
            self._service_log(f"Applied action: {action}, got expression: {expression}", "apply_action", 4)
            return expression, f"{left_str} {action_description} {right_str}"
        """

    def _service_extend_equation(self, left, right, left_str, right_str):
        """
        Procedure that generates expression to extend equation, 'randomly' selects an action and applies
            this action and extension to left and right parts of our equation for complication.
        :param left:
        :param right:
        :param left_str:
        :param right_str:
        :return:
        """
        actions = list(self.operation_probabilities.keys())
        weights = list(self.operation_probabilities.values())
        extend, extend_str = self._service_generator()
        self._service_log(f"Generated extend expression: {extend}", "extend_equation", 4)
        if self._service_not_val_or_symbol(extend):
            extend_str = f"({extend_str})"
        action = random.choices(actions, weights=weights)[0]
        self._service_log(f"Generated action: {action}", "extend_equation", 4)
        action_description = self._service_get_operation_description(action)
        if action == "add":
            if self.positive_flag:
                left = left + extend
                right = right + extend
            left_str = f"{left_str} {action_description} {extend_str}"
            right_str = f"{right_str} {action_description} {extend_str}"
            self.resolve_path.insert(0, f"- Subtract from both parts of equation {extend}")
            return left, right, left_str, right_str
        if action == "sub":
            # Numerator = numerator + denominator * expression
            # Denominator  = denominator
            if self.positive_flag:
                left = left - extend
                right = right - extend
            left_str = f"{left_str} {action_description} {extend_str}"
            right_str = f"{right_str} {action_description} {extend_str}"
            self.resolve_path.insert(0, f"- Add to both parts of equation {extend}")
            return left, right, left_str, right_str
        if action == "multiply":
            if self._service_not_val_or_symbol(left):
                left_str = f"({left_str})"
            if self._service_not_val_or_symbol(right):
                right_str = f"({right_str})"
            if self.positive_flag:
                left = left * extend
                right = right * extend
            left_str = f"{left_str} {action_description} {extend_str}"
            right_str = f"{right_str} {action_description} {extend_str}"
            self.resolve_path.insert(0, f"- Divide both parts of equation by {extend}")
            return left, right, left_str, right_str
        if action == "divide":
            if self._service_not_val_or_symbol(left):
                left_str = f"({left_str})"
            if self._service_not_val_or_symbol(right):
                right_str = f"({right_str})"
            if self.positive_flag:
                try:
                    left = left / extend
                    right = right / extend
                except ZeroDivisionError:
                    self.positive_flag = False
                    self.result = 0
                    self.error_type = "ZeroDivisionError"
                    self._service_log(f"Error type ZeroDivisionError for action: {action} ", "extend_equation", 1)
            left_str = f"{left_str} {action_description} {extend_str}"
            right_str = f"{right_str} {action_description} {extend_str}"
            self.resolve_path.insert(0, f"- Multiply both parts of equation by {extend}")
            return left, right, left_str, right_str
        if action == "power":
            if self._service_not_val_or_symbol(left):
                left_str = f"({left_str})"
            if self._service_not_val_or_symbol(right):
                right_str = f"({right_str})"
            left_str = f"{left_str} {action_description} {extend_str}"
            right_str = f"{right_str} {action_description} {extend_str}"
            if self.positive_flag:
                try:
                    left = left ** extend
                    right = right ** extend
                except ZeroDivisionError:
                    self.positive_flag = False
                    self.result = 0
                    self.error_type = "ZeroDivisionError"
                    self._service_log(f"Error type ZeroDivisionError for action: {action} ", "extend_equation", 1)
                except OverflowError:
                    self.positive_flag = False
                    self.result = 0
                    self.error_type = "OverflowError"
                    self._service_log(f"Error type OverflowError for action: {action} ", "extend_equation", 1)
            self.resolve_path.insert(0, f"- Power both parts of equation by 1/{extend}")
            return left, right, left_str, right_str
        # <TBD> logarithm, exponent, trigonometry

    def _service_generator(self):
        """
        Generator of expressions. From 'randomly' selected values and symbols builds and expression.
        :return:
        - expression in sympy format
        - expression in string representation
        """
        actions = list(self.operation_probabilities.keys())
        weights = list(self.operation_probabilities.values())
        actual_length = random.randint(self.expression_length[0], self.expression_length[1])
        left, left_str = self._service_get_symbol_or_value()
        right, right_str = self._service_get_symbol_or_value()
        for _ in range(actual_length):
            action = random.choices(actions, weights=weights)[0]
            left, left_str = self._service_apply_action(left, right, left_str, right_str, action)
            right, right_str = self._service_get_symbol_or_value()
        return left, left_str

    def _service_generate_expression(self):
        """
        Procedure for generating initial expression by type. Since type applies requirements to possible
            combinations of symbols and values, not all operations can be randomized.
        :return:
        - Expression left side in sympy format
        - Expression right side in sympy format
        - Expression left side in String format
        - Expression right side in String format
        """
        if self.equation_type == "linear":
            expr = 0
            expr_str = "0 + "
            for symbol_val in list(self.symbol_probabilities.keys()):
                # Generate coefficients of expression
                val_a, val_a_str = self._service_generate_value()
                # Generate operations description of expression
                operation_mul = self._service_get_operation_description("multiply")
                operation_add = self._service_get_operation_description("add")

                expr += val_a * symbol_val
                expr_str += f"{val_a_str} {operation_mul} {symbol_val} {operation_add} "
            val_c, val_c_str = self._service_generate_value()
            expr += val_c
            expr_str += val_c_str
            expression_left = expr
            expression_right = 0
            expression_left_str = expr_str
            expression_right_str = "0 "
        elif self.equation_type == "quadratic":
            expr = 0
            expr_str = "0 + "
            for symbol_val in list(self.symbol_probabilities.keys()):
                # Generate coefficients of expression
                val_a, val_a_str = self._service_generate_value()
                val_b, val_b_str = self._service_generate_value()
                # Generate operations description of expression
                operation_mul_1 = self._service_get_operation_description("multiply")
                operation_power = self._service_get_operation_description("power")
                operation_add_1 = self._service_get_operation_description("add")
                operation_mul_2 = self._service_get_operation_description("multiply")
                operation_add_2 = self._service_get_operation_description("add")

                expr += val_a * symbol_val ** 2 + val_b * symbol_val
                expr_str += f"{val_a_str} {operation_mul_1} {symbol_val} {operation_power} 2 {operation_add_1}\
                            {val_b_str}  {operation_mul_2} {symbol_val} {operation_add_2}"
            val_c, val_c_str = self._service_generate_value()
            expr += val_c
            expr_str += val_c_str
            expression_left = expr
            expression_right = 0
            expression_left_str = expr_str
            expression_right_str = "0 "
        elif self.equation_type == "cubic":
            expr = 0
            expr_str = "0 + "
            for symbol_val in list(self.symbol_probabilities.keys()):
                # Generate coefficients of expression
                val_a, val_a_str = self._service_generate_value()
                val_b, val_b_str = self._service_generate_value()
                val_c, val_c_str = self._service_generate_value()
                # Generate operations description of expression
                operation_mul_1 = self._service_get_operation_description("multiply")
                operation_power_1 = self._service_get_operation_description("power")
                operation_add_1 = self._service_get_operation_description("add")
                operation_mul_2 = self._service_get_operation_description("multiply")
                operation_power_2 = self._service_get_operation_description("power")
                operation_add_2 = self._service_get_operation_description("add")
                operation_mul_3 = self._service_get_operation_description("multiply")
                operation_add_3 = self._service_get_operation_description("add")

                expr += val_a * symbol_val ** 3 + val_b * symbol_val ** 2 + val_c * symbol_val
                expr_str += f"{val_a} {operation_mul_1} {symbol_val} {operation_power_1} 3 {operation_add_1} \
                              {val_b_str} {operation_mul_2} {symbol_val} {operation_power_2} 2 {operation_add_2} \
                              {val_c_str} {operation_mul_3} {symbol_val} {operation_add_3}"
            val_d, val_d_str = self._service_generate_value()
            expr += val_d
            expr_str += f"{val_d_str}"
            expression_left = expr
            expression_right = 0
            expression_left_str = expr_str
            expression_right_str = "0 "
        else:
            expression_left, expression_left_str = self._service_generator()
            expression_right, expression_right_str = self._service_generator()
        return expression_left, expression_right, expression_left_str, expression_right_str

    def _service_clean(self, regenerate_init):
        """
        Clear config and output for dynamically calculated and filled values.
        :return:
        none
        """
        self.equation = 0
        self.equation_str = ""
        self.resolve_path = []
        self.result = 0
        self.positive_flag = True
        self.error_type = ""
        if regenerate_init:
            self.init_expression = ""
            self.init_expression_str = ""

    def generate_equation(self, regenerate_init=True):
        """
        Generates equation in the following way:
        1. if regenerate_init == True, then 'randomly' generate initial expression. If not - use available
            init_expression.
        2. 'Randomly' define depth of the equation complication
        3. 'Randomly' generate expression for complication, and action. Using them, following algebra rules complicate
            the equation. Add text description of complication result to self.resolving_path.
        4. IMPORTANT:  Sympy automatically treats operands as expressions, and so a+b and c+d with action multiply
        will be (a+b) * (c+d)
        Defines state of the class instance with :
        :self.positive_flag: If True - expression is for positive test and expected result = self.result. If False -
            it is Negative Test and return saying that equation can not be calculated due to self.error_type
        :self.error_type: Error type for Negative test equation.
        :self.equation: String representation of equation where operands selected from self.operation_operands variants
        :self.eval_equation: String representation of equation in 'ready for python eval' format
        :self.latex_equation: String representation of LaTeX format.
        :self.result: Expected result for Positive tests or 0 for Negative

        :return:
        none
        """
        # Generate init expression. Expression is left=right
        # left = (numerator, denominator), right = (numerator, denominator)
        self._service_clean(regenerate_init)
        if regenerate_init:
            left, right, left_str, right_str = self._service_generate_expression()
            self.init_expression = (left, right)
            self.init_expression_str = (left_str, right_str)
        else:
            # <TBDF> NOT SUPPORTED YET
            left, right = self.init_expression
            left_str, right_str = self.init_expression_str
        self._service_log(f"Initial left: {left}", "generate_equation", 2)
        self._service_log(f"Initial right: {right}", "generate_equation", 2)
        self._service_log(f"Initial left_str: {left_str}", "generate_equation", 2)
        self._service_log(f"Initial right_str: {right_str}", "generate_equation", 2)
        try:
            self.result = sympy.solve(left - right, dict=True)
        except ValueError:
            self.result = 0
            self.positive_flag = False
            self.error_type = "ValueError"
            self._service_log(f"Error type ValueError for solving init expression: {left} - {right} ",
                              "generate_equation", 1)
        except NotImplementedError:
            self.result = 0
            self.positive_flag = False
            self.error_type = "NotImplementedError"
            self._service_log(f"Error type NotImplementedError for solving init expression: {left} - {right} ",
                              "generate_equation", 1)

        actual_depth = random.randint(self.complication_depth[0], self.complication_depth[1])
        for _ in range(actual_depth):
            left, right, left_str, right_str = self._service_extend_equation(left, right, left_str, right_str)
        if not self.positive_flag:
            left = 0
            right = 0
        self.equation = (left, right)
        self.equation_str = (left_str, right_str)

    def get_equation_type(self):
        return self.equation_type

    def set_equation_type(self, equation_type):
        if equation_type not in self.supported_equation_types:
            raise ValueError(f"ERROR: Type {equation_type} not in list of supported types.")
        self.equation_type = equation_type

    def get_supported_equation_types(self):
        return self.supported_equation_types

    def set_complication_depth(self, values):
        if not isinstance(values, tuple):
            raise ValueError("ERROR: Complication Depth should be a tuple")
        if len(values) != 2:
            raise ValueError("ERROR: Complication Depth should be a tuple containing exactly 2 values")
        if values[0] > values[1]:
            raise ValueError("ERROR: Complication Depth should be a tuple (min,max)")
        if values[0] <= 0 or values[1] <= 0:
            raise ValueError("ERROR: Complication Depth should be bigger than 0")
        if values[1] > 100:
            raise ValueError("ERROR: It is recommended to use less than 100 Complication Depth")
        self.complication_depth = values

    def get_complication_depth(self):
        return self.complication_depth

    def set_expression_length(self, values):
        if not isinstance(values, tuple):
            raise ValueError("ERROR: Expression Length should be a tuple")
        if len(values) != 2:
            raise ValueError("ERROR: Expression Length should be a tuple containing exactly 2 values")
        if values[0] > values[1]:
            raise ValueError("ERROR: Expression Length should be a tuple (min,max)")
        if values[0] <= 0 or values[1] <= 0:
            raise ValueError("ERROR: Expression Length should be bigger than 0")
        if values[1] > 100:
            raise ValueError("ERROR: It is recommended to use less than 100 Expression Length")
        self.expression_length = values

    def get_expression_length(self):
        return self.expression_length

    def get_types(self):
        return list(self.type_ranges.keys())

    def set_type_ranges(self, ranges):
        if not isinstance(ranges, dict):
            raise TypeError("ERROR: Type Ranges should be a dict")
        if len(ranges) == 0:
            raise ValueError("ERROR: Type Ranges should contain at least 1 entry")
        for single_range in ranges:
            if not isinstance(ranges[single_range], tuple):
                raise ValueError(f"ERROR: Type Ranges for {single_range} should be a tuple")
            if len(ranges[single_range]) != 2:
                raise ValueError(f"ERROR: Type Ranges for {single_range} should be a tuple containing exactly 2 values")
            if single_range == "float":
                if not isinstance(ranges[single_range][0], float) or not isinstance(ranges[single_range][1], float):
                    raise TypeError("ERROR: Float ranges should be float.")
            if single_range == "integer":
                if not isinstance(ranges[single_range][0], int) or not isinstance(ranges[single_range][1], int):
                    raise TypeError("ERROR: Int ranges should be int.")
            if single_range != "fraction":
                if ranges[single_range][0] > ranges[single_range][1]:
                    raise ValueError(f"ERROR: Type Ranges for {single_range} should be a tuple (min,max)")
            if single_range == "fraction":
                if not isinstance(ranges[single_range][0], tuple) or not isinstance(ranges[single_range][1], tuple):
                    raise ValueError(f"ERROR: Type Ranges for {single_range} should be a tuple ((min,max), (min, max))")
                if not isinstance(ranges[single_range][0][0], int) or not isinstance(ranges[single_range][0][1], int) \
                        or not isinstance(ranges[single_range][1][0], int) \
                        or not isinstance(ranges[single_range][1][1], int):
                    raise TypeError("ERROR: Fraction ranges should be int.")
                if ranges[single_range][0][0] > ranges[single_range][0][1] or \
                        ranges[single_range][1][0] > ranges[single_range][1][1]:
                    raise ValueError(f"ERROR: Type Ranges for {single_range} should be in form ((min,max), (min, max))")
        self.type_ranges = ranges.copy()

    def get_type_ranges(self):
        return self.type_ranges

    def set_type_probabilities(self, probabilities):
        if not isinstance(probabilities, list):
            raise TypeError("ERROR: Type Probabilities should be a list")
        for probability in probabilities:
            if not isinstance(probability, float):
                raise TypeError(f"ERROR: Type Probability {probability} should be a float")
            if probability < 0.0 or probability > 1.0:
                raise ValueError(f"ERROR: Type Probability {probability} should be in the range 0.0 <= prob <=1.0")
        self.type_probabilities = probabilities.copy()

    def get_type_probabilities(self):
        return self.type_probabilities

    def set_symbol_probabilities(self, probabilities):
        if not isinstance(probabilities, dict):
            raise TypeError("ERROR: Type Probabilities should be a list")
        if len(list(probabilities.keys())) < 1:
            raise ValueError(f"ERROR: Symbol Probability must have at least 1 symbol of sympy.Symbol type")
        for key_val in list(probabilities.keys()):
            if not isinstance(key_val, sympy.Symbol):
                raise TypeError(f"ERROR: Symbol Probability key {key_val} must be of sympy.Symbol type")
        for probability in probabilities:
            if not isinstance(probabilities[probability], float):
                raise TypeError(f"ERROR: Type Probability {probability} value should be a float")
            if probabilities[probability] < 0.0 or probabilities[probability] > 1.0:
                raise ValueError(f"ERROR: Type Probability {probability} should be in the range 0.0 <= prob <=1.0")
        self.symbol_probabilities = probabilities.copy()

    def get_symbol_probabilities(self):
        return self.symbol_probabilities

    def set_operation_probabilities(self, probabilities):
        if not isinstance(probabilities, dict):
            raise TypeError("ERROR: Operation probabilities must be a dict")
        if len(probabilities) == 0:
            raise ValueError(f"ERROR: Operation probabilities should contain at least 1 value")
        for operation in probabilities:
            if not isinstance(probabilities[operation], float):
                raise TypeError(f"ERROR: Operation {operation} probability must be float 0.0<= prob <=1.0")
            if probabilities[operation] < 0.0 or probabilities[operation] > 1.0:
                raise ValueError(f"ERROR: Operation {operation} probabilities range is 0 <= prob <= 1.0")
        self.operation_probabilities = probabilities.copy()

    def get_operation_probabilities(self):
        return self.operation_probabilities

    def set_operation_operands(self, operands):
        if not isinstance(operands, dict):
            raise ValueError("ERROR: Operation operands must be a dict")
        self.operation_operands = operands.copy()

    def get_operation_operands(self):
        return self.operation_operands

    def set_symbols_density(self, probability):
        if not isinstance(probability, float):
            raise TypeError("ERROR: Symbols Density must be float.")
        if probability < 0.0 or probability > 1.0:
            raise ValueError("ERROR: Symbols Density must be in range 0.0 <= prob <= 1.0 .")
        self.symbols_density = probability

    def get_symbols_density(self):
        return self.symbols_density

    def get_info(self):
        return self.equation, self.result

    def get_equation(self):
        return self.equation

    def get_string_equation(self):
        return self.equation_str

    def get_init_expression(self):
        return self.init_expression

    def _set_init_expression(self, expression):
        """
        <TBD> needs to be re-considered, because should be in sync with text description of initial expression.
        Prepare equation in sympy format. Be sure first to set_symbol_probabilities with probabilities for sympy.Symbol
        same as in this equation.
        """
        if not isinstance(expression, tuple):
            raise TypeError("ERROR: Initial expression must be an expression in tuple form (left side, right side)")
        if len(expression) != 2:
            raise TypeError("ERROR: Initial expression must be a tuple with exactly 2 options(left side, right side)")
        self.init_expression = expression

    def get_init_expression_string(self):
        return self.init_expression_str

    def _set_init_expression_string(self, expression):
        """
        <TBD> - needs to be re-considered, because should be in sync with sympy description of initial expression.
        Prepare equation in sympy format. Be sure first to set_symbol_probabilities with probabilities for sympy.Symbol
        same as in this equation.
        """
        if not isinstance(expression, tuple):
            raise TypeError("ERROR: Initial expression as string must be a tuple ('left side', 'right side')")
        if len(expression) != 2:
            raise TypeError("ERROR: Initial expression as string must have exactly 2 values('left side', 'right side')")
        self.init_expression_str = expression

    def get_result(self):
        return self.positive_flag, self.result, self.error_type

    def get_resolve_path(self):
        return self.resolve_path

    def set_log_level(self, level):
        if not isinstance(level, int):
            raise TypeError("ERROR: Log level must be between 0 and 5")
        if level < 0 or level > 5:
            raise ValueError("ERROR: Log level must be between 0 and 5")
        self.log_level = level

    def get_log_level(self):
        return self.log_level

