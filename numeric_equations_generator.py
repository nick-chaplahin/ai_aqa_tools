"""
Automatic complex equations generator.
Author: Nick  Chaplahin, 2025
Copyright: Nick Chaplahin


Configurable:
- number of values in equation
- values types, probabilities to appear in equation,  and ranges. On adding new types add its support in
     _service_generate_value()
- operations of equation.  On adding new operations add its support to _service_apply_action()
- probabilities of operands to appear in equation

Can be read:
- equation in string format with textual description
- equation in Python math format ready for eval/calculation
- equation in LaTeX format
- result of equation calculation, type of Test (Positive/Negative) and error type for Negative.
"""
import fractions
import math  # math import is required for eval execution when math.log, math.e or any other math.xxx available.
import random


class EquationGenerator:

    def __init__(self):
        # Configuration parameters
        self.values_num = (20, 25)
        self.type_probabilities = [0.4, 0.4, 0.2]  # [integer, float, fraction]
        self.type_ranges = {
            "integer": (-200, 200),
            "float": (-200.0, 200.0),
            "fraction": ((-200, 200), (-400, 400))
        }
        self.operation_probabilities = {
            'add': 0.25,
            'sub': 0.25,
            'multiply': 0.15,
            'divide': 0.15,
            'power': 0.1,
            'logarithm': 0.05,
            'euler_num': 0.05
        }
        self.operation_operands = {
            'add': '+',
            'sub': '-',
            'multiply': '*',
            'divide': '/',
            'power': ' ** ',
            'logarithm': 'log({}, {})',
            'euler_num': '{} * e^({})'
        }
        self.expression_probability = 0.3
        self.positive_flag = True
        self.error_type = ""
        self.equation = ""
        self.latex_equation = ""
        self.eval_equation = ""
        self.result = 0
        # Generate equation
        self.generate_equation()

    def _service_generate_value(self):
        """
           According to self.type_probabilities selects value of variable type. Then generates a 'random' value
        withing configured boundaries for a type self.type_ranges.
        :return:
        - string representation of the value,
        - LaTex representation of the value in String format,
        - numerical representation of the value, for fractions in fractions.Fraction type
        """
        types = list(self.type_ranges.keys())
        value_type = random.choices(types, weights=self.type_probabilities)[0]

        if value_type == "integer":
            num = random.randint(self.type_ranges["integer"][0], self.type_ranges["integer"][1])
            while num == 0:
                num = random.randint(self.type_ranges["integer"][0], self.type_ranges["integer"][1])
            return {'str': str(num), 'eval_str': str(num), 'latex_str': str(num), 'num': num}
        elif value_type == 'float':
            num = round(random.uniform(self.type_ranges["float"][0], self.type_ranges["float"][1]), 5)
            while num == 0.0:
                num = round(random.uniform(self.type_ranges["float"][0], self.type_ranges["float"][1]), 5)
            return {'str': f"{num:.5f}", 'eval_str': f"{num:.5f}", 'latex_str': f"{num:.5f}", 'num': num}
        else:  # fraction
            numerator = random.randint(self.type_ranges["fraction"][0][0], self.type_ranges["fraction"][0][1])
            while numerator == 0:
                numerator = random.randint(self.type_ranges["fraction"][0][0], self.type_ranges["fraction"][0][1])
            denominator = random.randint(self.type_ranges["fraction"][1][0], self.type_ranges["fraction"][1][1])
            while denominator == 0:
                denominator = random.randint(self.type_ranges["fraction"][1][0], self.type_ranges["fraction"][1][1])
            num = fractions.Fraction(numerator, denominator)
            str_val = f"({num.numerator}/{num.denominator})"
            return {'str': str_val, 'eval_str': str_val,
                    'latex_str': f"\\frac{{{num.numerator}}}{{{num.denominator}}}", 'num': num}

    def _service_apply_action(self, left, right, action):
        """
            Procedure to generate a part of equation around single operator. Each operation schematically can be
        represented as '{} action {}'. So left is left operand (value or part of equation), right is right operand
        (value or part of the equation), and action is an operator.
           Note: can be specific cases like exponent and log.
        exponent is e^{}, to simplify code it is being build as {left} * e^{right}. TBD - add dynamic selection of
        operand instead of '*'
        log is log({value}, {base}), where {base} = {left} and {value} = {right}

        :param left: left operand for action
        :param right: right operand for action
        :param action: math operation
        :return:
           - String of math operation description where action is replaced by 'random' "self.operation_operands"
           for this action
           - Ready-for-Python-eval-string of {left operand} {action} {right operand} in python math format.
        (exponent = {lef}*math.e ** ({right}) log = math.log({right}, {left}).
           - String that represents equation in LaTeX format
           - Computed result of this peace of equation if computable, or 0 if not.
        """
        left_str, left_eval, left_latex, left_num = left['str'], left['eval_str'], \
            left['latex_str'], left['num']
        right_str, right_eval, right_latex, right_num = right['str'], right['eval_str'], \
            right['latex_str'], right['num']
        # 'Randomly' selecting one of textual representation of the action from configurable operation_operands dict
        if isinstance(self.operation_operands[action], list):
            action_description = random.choice(self.operation_operands[action])
        else:
            action_description = self.operation_operands[action]
        # To store result of calculation of this peace of equation, if computable
        tmp_result = 0
        # For each configured action type forming string with equation peace and trying to compute it.
        if action == 'add':
            if self.positive_flag:
                try:
                    tmp_result = left_num + right_num
                except OverflowError:
                    self.positive_flag = False
                    self.error_type = "OverflowError"
                    tmp_result = 0
            return f"{left_str} {action_description} {right_str}", f"{left_eval} + {right_eval}", \
                f"{left_latex} + {right_latex}", tmp_result
        elif action == 'sub':
            if self.positive_flag:
                try:
                    tmp_result = left_num - right_num
                except OverflowError:
                    self.positive_flag = False
                    self.error_type = "OverflowError"
                    tmp_result = 0
            return f"{left_str} {action_description} {right_str}", f"{left_eval} - {right_eval}", \
                f"{left_latex} - {right_latex}", tmp_result
        elif action == 'multiply':
            if self.positive_flag:
                try:
                    tmp_result = left_num * right_num
                except OverflowError:
                    self.positive_flag = False
                    self.error_type = "OverflowError"
                    tmp_result = 0
            return f"{left_str} {action_description} {right_str}", f"{left_eval} * {right_eval}", \
                f"{left_latex} * {right_latex}", tmp_result
        elif action == 'divide':
            if self.positive_flag:
                try:
                    tmp_result = left_num / right_num
                except ZeroDivisionError:
                    self.positive_flag = False
                    self.error_type = "ZeroDivisionError"
                    tmp_result = 0
                except OverflowError:
                    self.positive_flag = False
                    self.error_type = "OverflowError"
                    tmp_result = 0
            return f"{left_str} {action_description} {right_str}", f"{left_eval} / {right_eval}", \
                f"{left_latex} / {right_latex}", tmp_result
        elif action == 'power':
            if self.positive_flag:
                try:
                    tmp_result = left_num / right_num
                except ValueError:
                    self.positive_flag = False
                    self.error_type = "ValueError"
                    tmp_result = 0
                except OverflowError:
                    self.positive_flag = False
                    self.error_type = "OverflowError"
                    tmp_result = 0
                except ZeroDivisionError:
                    self.positive_flag = False
                    self.error_type = "ZeroDivisionError"
                    tmp_result = 0
            return f"{left_str}{action_description}{right_str}", \
                f"{left_eval} ** {right_eval}", f"{left_latex}^{right_latex}", tmp_result
        elif action == 'logarithm':
            """
               In math logarithm is LOG_base_EXPRESSION, this is why {base} = {left} and {expression} = {right}
            In Python logarithm is math.log({expression}, {base}).  Keep this in mind
            In LaTeX logarithm is '\log_base expression'.
               Important!: In LaTeX {base} must be wrapped to {{{ }}} because math.log treats all
            {left} expression as {base}, and expression must be wrapped in ( ) because math.log treats all {right} 
            as expression.
            """
            if self.positive_flag:
                try:
                    if isinstance(left_num, complex) or isinstance(right_num, complex):
                        self.positive_flag = False
                        self.error_type = "ValueError"
                        tmp_result = 0
                    elif left_num <= 0 or left_num == 1 or right_num <= 0:
                        self.positive_flag = False
                        self.error_type = "ValueError"
                        tmp_result = 0
                    else:
                        tmp_result = eval(f"math.log({right_eval}, {left_eval})")
                except ValueError:
                    self.positive_flag = False
                    self.error_type = "ValueError"
                    tmp_result = 0
                except OverflowError:
                    self.positive_flag = False
                    self.error_type = "OverflowError"
                    tmp_result = 0
                except ZeroDivisionError:
                    self.positive_flag = False
                    self.error_type = "ZeroDivisionError"
                    tmp_result = 0
                except TypeError:
                    self.positive_flag = False
                    self.error_type = "TypeError"
                    tmp_result = 0
            return action_description.format(right_str, left_str), \
                f"math.log({right_eval}, {left_eval})", f"\\log_{{{left_latex}}}({right_latex})", tmp_result
        elif action == 'euler_num':
            """
               To avoid misunderstanding, exponent is e^{expression}, since this format is {left} * e ** {right} it
            will be more correct to call e euler num because formed and calculated expression 'num * e^ num'
            TBD:  make '*' operation configurable or 'random' selection between '+=*/'. 
            """
            if self.positive_flag:
                try:
                    tmp_result = eval(f"{left_eval} * math.e ** ({right_eval})")
                except ValueError:
                    self.positive_flag = False
                    self.error_type = "ValueError"
                    tmp_result = 0
                except OverflowError:
                    self.positive_flag = False
                    self.error_type = "OverflowError"
                    tmp_result = 0
                except TypeError:
                    self.positive_flag = False
                    self.error_type = "TypeError"
                    tmp_result = 0
                except ZeroDivisionError:
                    self.positive_flag = False
                    self.error_type = "ZeroDivisionError"
                    tmp_result = 0
            return action_description.format(left_str, right_str), \
                f"{left_eval} * math.e ** ({right_eval})", f"{left_latex} * e^{{{right_latex}}}", tmp_result

    def _service_clean(self):
        """
        Since Class keeps its values to be able to called as many times as needed  - here clearing 'returns'.
        :return:
        none
        """
        self.positive_flag = True
        self.error_type = ""
        self.eval_equation = ""
        self.equation = ""
        self.latex_equation = ""

    def generate_equation(self):
        """
           Generates equation in the following way:
        1. 'Randomly' defines list of values to use.
        2. 'Randomly' defines an action from list of actions
        3. 'Randomly selects 2 elements of 'values' and creates an expression with them. Used values removed
        4. Adds 'expression as value back to values.
        5. IMPORTANT:  if one generated expression is 'a + b' and other is 'c + d',
           and they are selected as operands for action '*', then final  expression will be 'a + b * c + d'.
           Unless during generation expression_probability happened, and if it happened to 'a+b' it become '(a+b)' and ]
           then final expression will be (a+b) * c + d
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
        self._service_clean()
        actions = list(self.operation_probabilities.keys())
        weights = list(self.operation_probabilities.values())
        values_num = random.randint(self.values_num[0], self.values_num[1])
        values = [self._service_generate_value() for _ in range(values_num)]
        while len(values) > 1:
            i = random.randint(0, len(values) - 2)
            left = values.pop(i)
            right = values.pop(i)
            action = random.choices(actions, weights=weights)[0]
            new_str, new_eval, new_latex, new_num = self._service_apply_action(left, right, action)
            if random.random() < self.expression_probability:
                new_str = f"({new_str})"
                new_eval = f"({new_eval})"
                new_latex = f"({new_latex})"
            values.insert(i, {'str': new_str, 'eval_str': new_eval, 'latex_str': new_latex, 'num': new_num})

        self.equation = values[0]['str']
        self.latex_equation = f"${values[0]['latex_str']}$"
        self.eval_equation = values[0]['eval_str']
        if self.positive_flag:
            try:
                self.result = eval(values[0]['eval_str'])
            except ZeroDivisionError:
                self.result = 0
                self.positive_flag = False
                self.error_type = "ZeroDivisionError"
            except OverflowError:
                self.result = 0
                self.positive_flag = False
                self.error_type = "OverflowError"
        else:
            self.result = 0

    # ===== Setters and Getters to configure class and get the result.=====
    def set_values_num(self, values):
        if not isinstance(values, tuple):
            raise TypeError("ERROR: values should be a tuple")
        if len(values) != 2:
            raise ValueError("ERROR: values should be a tuple containing exactly 2 values")
        if not isinstance(values[0], int) or not isinstance(values[1], int):
            raise TypeError("ERROR: values should be integer")
        if values[0] > values[1]:
            raise ValueError("ERROR: values should be a tuple (min, max)")
        if values[0] <= 0 or values[1] <= 0:
            raise ValueError("ERROR: values should be bigger than 0")
        if values[1] > 100:
            raise ValueError("ERROR: It is recommended to generate less than 100 values")
        self.values_num = values

    def get_values_num(self):
        return self.values_num

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

    def get_type_ranges(self):
        return self.type_ranges

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

    def set_expression_probability(self, probability):
        if not isinstance(probability, float):
            raise TypeError("ERROR: Expression Probability must be float.")
        if probability < 0.0 or probability > 1.0:
            raise ValueError("ERROR: Expression Probability must be in range 0.0 <= prob <= 1.0 .")
        self.expression_probability = probability

    def get_expression_probability(self):
        return self.expression_probability

    def get_info(self):
        return self.equation, self.result

    def get_equation(self):
        return self.equation

    def get_latex_equation(self):
        return self.latex_equation

    def get_eval_equation(self):
        return self.eval_equation

    def get_result(self):
        """

        :return:
        - positive test flag: if True - test is Positive, otherwise Negative
        - result: Numeric value for equation result if equation computable, and 0 is not
        - error type: Type of error that raised during calculation, can be compared to AI's replies if
           error types returned
        """
        return self.positive_flag, self.result, self.error_type
