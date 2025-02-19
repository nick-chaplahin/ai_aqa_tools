"""
Tests for Complex equations generator usage
Author: Nick  Chaplahin, 2025
Copyright: Nick Chaplahin

License: MIT

Requires PyTest!
"""

import pytest
import sympy
from algebraic_equations_generator import AlgebraicEquationGenerator

equation_types_positive_test_data = [
    "linear",
    "quadratic",
    "cubic",
    "general"
]
equation_types_negative_test_data = [
    "some",
    "qubic",
    3,
    ["quadratic", "cubic"]
]

expression_length_positive_test_data = [
    (1, 5),
    (2, 8),
    (4, 12),
    (20, 90)
]
expression_length_negative_test_data = [
    2,
    (-1, 5),
    (0, 8),
    (-4, -1),
    (10, 6),
    (100, 200),
    ("a", "b"),
    ["a", "b"]
]
complication_depth_positive_test_data = [
    (1, 5),
    (2, 8),
    (4, 12),
    (20, 90)
]
complication_depth_negative_test_data = [
    2,
    (-1, 5),
    (0, 8),
    (-4, -1),
    (10, 6),
    (100, 200),
    ("a", "b"),
    ["a", "b"]
]
type_probabilities_positive_test_data = [
    [0.1, 0.4, 0.2],
    [0.1],
    [1.0],
    [0.0],
    [0.9, 0.05, 0.05]

]
type_probabilities_negative_test_data = [
    0.4,
    {0.4: 0.5},
    [0.1, 2, 0.3],
    [-0.2, 0.4],
    [-0.1, -0.2, -0.3],
    [0.9, "a", "c"],
    [1, 2, 3]

]
# IMPORTANT: List of types should include supported types: integer, float, fraction
type_ranges_positive_test_data = [
    {"integer": (-100, 100), "float": (-100.0, 100.0), "fraction": ((-100, 100), (200, 400))},
    {"integer": (-100, 100), "float": (-100.0, 100.0)},
    {"fraction": ((-100, 100), (200, 400))},
    {"integer": (-1000, 1000), "float": (-1000.0, 1000.0), "fraction": ((-1000, 1000), (2000, 4000))},
    {"integer": (-1000, -100), "float": (-1000.0, -100.0), "fraction": ((-1000, -100), (-200, -40))},
    {"integer": (100, 1000), "float": (100.0, 1000.0), "fraction": ((100, 1000), (200, 400))}
]
# IMPORTANT: List of types should include supported types: integer, float, fraction
type_ranges_negative_test_data = [
    [(-100, 100), (-100.0, 100.0), ((-100, 100), (200, 400))],
    {},
    {"integer": (-100, 100), "float": (), "fraction": ((-100, 100), (200, 400))},
    {"integer": (100, -100), "float": (100.0, -100.0), "fraction": ((100, -100), (200, 400))},
    {"integer": (-100), "float": (-100.0, 100.0), "fraction": (-100, 400)},
    {"integer": (-100, 100), "float": (-100.0, 100.0), "fraction": (-100, 400)},
    {"integer": ("b", "a")},
    {"integer": (-100.1, 100.1)},
    {"float": ("b", "a")},
    {"float": (-100, 100)},
    {"fraction": (("b", "a"), ("d", "c"))},
    {"fraction": ((-100.0, 100.0), (-20.0, 20.0))}
]
# IMPORTANT: List of operations should include supported operations, in current version are:
# add, sub, multiply, divide, power, logarithm, euler_num
oper_probabilities_positive_test_data = [
    {"add": 0.1, "sub": 0.1, "mul": 0.1},
    {"a": 0.3, "b": 0.5, "c": 0.4},
    {"add": 0.0, "sub": 0.1, "mul": 0.1},
    {"add": 1.0, "sub": 0.1, "mul": 0.1}
]
oper_probabilities_negative_test_data = [
    {"add": 10, "sub": 0.1, "mul": 0.1},
    {"add": "a", "sub": 0.1, "mul": 0.1},
    {},
    ["a", 0.1, 0.1],
    {"add": -0.2, "sub": 0.1, "mul": 0.1}

]
# IMPORTANT NOTE: There is no illegal operation operands, you can mess with them in any way you want for
# verification of system behaviour on invalid and/or meaningless strings.
# IMPORTANT: List of operations should include supported operations, in current version are:
# add, sub, multiply, divide, power, logarithm, euler_num
oper_operands_positive_test_data = [
    {'power': [' power to ', '^', '**'],
      'logarithm': ['logarithm of ({}) base ({})', 'log({},{})', 'log_({}) ({})', 'logarithm ({}) base ({})'],
      'euler_num': ['{} multiply by e power to ({})', '{} mul e^({})', '{} * e^({})', '{} mul by e ** ({})']},
    {'power': [1, 2, 4, 5],
      'logarithm': 132,
      'euler_num': ['abbaaga', 'CU', '4SUCCESS', 'NJOY']}
]
symbol_probabilities_positive_test_data = [
    {sympy.Symbol("x"): 0.1, sympy.Symbol("y"): 0.1, sympy.Symbol("z"): 0.1},
    {sympy.Symbol("x"): 0.9,  sympy.Symbol("z"): 0.1},
    {sympy.Symbol("x"): 0.2, sympy.Symbol("y"): 0.8 },
    {sympy.Symbol("x"): 1.0, sympy.Symbol("y"): 0.0, sympy.Symbol("z"): 0.0},
]
symbol_probabilities_negative_test_data = [
    {sympy.Symbol("x"): 0.1, sympy.Symbol("y"): 10, sympy.Symbol("z"): 0.1},
    {sympy.Symbol("x"): 0.1, sympy.Symbol("y"): 0.1, sympy.Symbol("z"): 1.1},
    {},
    ["a", 0.1, 0.1],
    {sympy.Symbol("x"): -0.1, sympy.Symbol("y"): 0.1, sympy.Symbol("z"): 0.1},

]
symbols_density_positive_test_data = [
    0.0,
    1.0,
    0.3,
    0.5
]
symbols_density_negative_test_data = [
    0,
    1,
    2,
    -0.2,
    "a",
    [0.3]
]

# IMPORTANT: self.init_expression and self.init_expression_str can not be set for now.

log_level_positive_test_data = [
    0,
    1,
    2,
    3,
    4,
    5
]
log_level_negative_test_data = [
    -1,
    -5,
    11,
    0.2,
    "a",
    [0.3]
]

# IMPORTANT: List of operations should include supported operations, in current version are:
# add, sub, multiply, divide, power, logarithm, euler_num
generate_equation_positive_test_data = [
    ({"add": '+'}, {"add": 1.0}, (2, 2), (2, 2), {"integer": (5, 5)}, [1.0], {sympy.Symbol("x"): 1.0}, 0.0,
     ('5 + 5 + 5 + 5 + 5 + 5 + 5 + 5 + 5', '5 + 5 + 5 + 5 + 5 + 5 + 5 + 5 + 5')),
    ({"add": 'plus'}, {"add": 1.0}, (2, 2), (2, 2), {"integer": (7, 7)}, [1.0], {sympy.Symbol("x"): 1.0}, 1.0,
     ('x plus x plus x plus (x plus x plus x) plus (x plus x plus x)',
      'x plus x plus x plus (x plus x plus x) plus (x plus x plus x)'))
]


@pytest.mark.parametrize("test_value", equation_types_positive_test_data)
def test_set_equation_types_positive(test_value):
    test_class = AlgebraicEquationGenerator()
    test_class.set_equation_type(test_value)
    configured_value = test_class.get_equation_type()
    assert configured_value == test_value


@pytest.mark.parametrize("test_value", equation_types_negative_test_data)
def test_set_equation_types_negative(test_value):
    test_class = AlgebraicEquationGenerator()
    with pytest.raises(Exception):
        test_class.set_equation_type(test_value)


@pytest.mark.parametrize("test_values", expression_length_positive_test_data)
def test_set_expression_length_positive(test_values):
    test_class = AlgebraicEquationGenerator()
    test_class.set_expression_length(test_values)
    configured_values = test_class.get_expression_length()
    assert configured_values[0] == test_values[0] and configured_values[1] == test_values[1]


@pytest.mark.parametrize("test_values", expression_length_negative_test_data)
def test_set_expression_length_negative(test_values):
    test_class = AlgebraicEquationGenerator()
    with pytest.raises(Exception):
        test_class.set_expression_length(test_values)


@pytest.mark.parametrize("test_values", complication_depth_positive_test_data)
def test_set_complication_depth_positive(test_values):
    test_class = AlgebraicEquationGenerator()
    test_class.set_complication_depth(test_values)
    configured_values = test_class.get_complication_depth()
    assert configured_values[0] == test_values[0] and configured_values[1] == test_values[1]


@pytest.mark.parametrize("test_values", complication_depth_negative_test_data)
def test_set_complication_depth_negative(test_values):
    test_class = AlgebraicEquationGenerator()
    with pytest.raises(Exception):
        test_class.set_complication_depth(test_values)


@pytest.mark.parametrize("test_values", type_probabilities_positive_test_data)
def test_set_type_probabilities_positive(test_values):
    test_class = AlgebraicEquationGenerator()
    test_class.set_type_probabilities(test_values)
    configured_values = test_class.get_type_probabilities()
    assert configured_values == test_values


@pytest.mark.parametrize("test_values", type_probabilities_negative_test_data)
def test_set_type_probabilities_negative(test_values):
    test_class = AlgebraicEquationGenerator()
    with pytest.raises(Exception):
        test_class.set_type_probabilities(test_values)


@pytest.mark.parametrize("test_values", type_ranges_positive_test_data)
def test_set_type_ranges_positive(test_values):
    test_class = AlgebraicEquationGenerator()
    test_class.set_type_ranges(test_values)
    configured_values = test_class.get_type_ranges()
    assert configured_values == test_values


@pytest.mark.parametrize("test_values", type_ranges_negative_test_data)
def test_set_type_ranges_negative(test_values):
    test_class = AlgebraicEquationGenerator()
    with pytest.raises(Exception):
        test_class.set_type_ranges(test_values)


@pytest.mark.parametrize("test_values", oper_probabilities_positive_test_data)
def test_set_operation_probabilities_positive(test_values):
    test_class = AlgebraicEquationGenerator()
    test_class.set_operation_probabilities(test_values)
    configured_values = test_class.get_operation_probabilities()
    assert configured_values == test_values


@pytest.mark.parametrize("test_values", oper_probabilities_negative_test_data)
def test_set_operation_probabilities_negative(test_values):
    test_class = AlgebraicEquationGenerator()
    with pytest.raises(Exception):
        test_class.set_operation_probabilities(test_values)


@pytest.mark.parametrize("test_values", oper_operands_positive_test_data)
def test_set_operation_operands_positive(test_values):
    test_class = AlgebraicEquationGenerator()
    test_class.set_operation_operands(test_values)
    configured_values = test_class.get_operation_operands()
    assert configured_values == test_values


@pytest.mark.parametrize("test_values", symbol_probabilities_positive_test_data)
def test_set_symbol_probabilities_positive(test_values):
    test_class = AlgebraicEquationGenerator()
    test_class.set_symbol_probabilities(test_values)
    configured_values = test_class.get_symbol_probabilities()
    assert configured_values == test_values


@pytest.mark.parametrize("test_values", symbol_probabilities_negative_test_data)
def test_set_symbol_probabilities_negative(test_values):
    test_class = AlgebraicEquationGenerator()
    with pytest.raises(Exception):
        test_class.set_symbol_probabilities(test_values)


@pytest.mark.parametrize("test_value", symbols_density_positive_test_data)
def test_set_symbols_density_positive(test_value):
    test_class = AlgebraicEquationGenerator()
    test_class.set_symbols_density(test_value)
    configured_value = test_class.get_symbols_density()
    assert configured_value == test_value


@pytest.mark.parametrize("test_value", symbols_density_negative_test_data)
def test_set_symbols_density_negative(test_value):
    test_class = AlgebraicEquationGenerator()
    with pytest.raises(Exception):
        test_class.set_symbols_density(test_value)


@pytest.mark.parametrize("test_value", log_level_positive_test_data)
def test_set_log_level_positive(test_value):
    test_class = AlgebraicEquationGenerator()
    test_class.set_log_level(test_value)
    configured_value = test_class.get_log_level()
    assert configured_value == test_value


@pytest.mark.parametrize("test_value", log_level_negative_test_data)
def test_set_log_level_negative(test_value):
    test_class = AlgebraicEquationGenerator()
    with pytest.raises(Exception):
        test_class.set_log_level(test_value)

@pytest.mark.parametrize("oper_operands, oper_probabilities, expression_length, complication_depth, type_ranges, type_probabilities,\
                         symbol_probabilities, symbols_density, expected",
                         generate_equation_positive_test_data)
def test_generate_equation_positive(oper_operands,
                                    oper_probabilities,
                                    expression_length,
                                    complication_depth,
                                    type_ranges,
                                    type_probabilities,
                                    symbol_probabilities,
                                    symbols_density,
                                    expected):
    test_class = AlgebraicEquationGenerator()
    test_class.set_operation_operands(oper_operands)
    test_class.set_operation_probabilities(oper_probabilities)
    test_class.set_expression_length(expression_length)
    test_class.set_complication_depth(complication_depth)
    test_class.set_type_ranges(type_ranges)
    test_class.set_type_probabilities(type_probabilities)
    test_class.set_symbol_probabilities(symbol_probabilities)
    test_class.set_symbols_density(symbols_density)
    test_class.set_equation_type("general")
    test_class.generate_equation()
    equation = test_class.get_string_equation()
    assert equation == expected
