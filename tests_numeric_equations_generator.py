"""
Tests for Complex equations generator usage
Author: Nick  Chaplahin, 2025
Copyright: Nick Chaplahin

License: MIT

Requires PyTest!
"""

import pytest
from numeric_equations_generator import EquationGenerator


values_num_positive_test_data = [
    (5, 10),
    (10, 30),
    (15, 15)
]
values_num_negative_test_data = [
    (30, 10),
    (0, 10),
    (-10, -2),
    (-10, 10),
    (1, 500),
    ("a", "b"),
    [10, 20],
    5
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
expression_probability_positive_test_data = [
    0.0,
    1.0,
    0.3,
    0.5
]
expression_probability_negative_test_data = [
    0,
    1,
    2,
    -0.2,
    "a",
    [0.3]
]
# IMPORTANT: List of operations should include supported operations, in current version are:
# add, sub, multiply, divide, power, logarithm, euler_num
generate_equation_positive_test_data = [
    ({"add": '+'}, {"add": 1.0}, (2, 2), {"integer": (5, 5)}, [1.0], 0.0, "5 + 5"),
    ({"add": 'plus'}, {"add": 1.0}, (2, 2), {"integer": (7, 7)}, [1.0], 1.0, "(7 plus 7)")
]


@pytest.mark.parametrize("test_values", values_num_positive_test_data)
def test_set_values_positive(test_values):
    test_class = EquationGenerator()
    test_class.set_values_num(test_values)
    configured_values = test_class.get_values_num()
    assert configured_values[0] == test_values[0] and configured_values[1] == test_values[1]


@pytest.mark.parametrize("test_values", values_num_negative_test_data)
def test_set_values_negative(test_values):
    test_class = EquationGenerator()
    with pytest.raises(Exception):
        test_class.set_values_num(test_values)


@pytest.mark.parametrize("test_values", type_ranges_positive_test_data)
def test_set_type_ranges_positive(test_values):
    test_class = EquationGenerator()
    test_class.set_type_ranges(test_values)
    configured_values = test_class.get_type_ranges()
    assert configured_values == test_values


@pytest.mark.parametrize("test_values", type_ranges_negative_test_data)
def test_set_type_ranges_negative(test_values):
    test_class = EquationGenerator()
    with pytest.raises(Exception):
        test_class.set_type_ranges(test_values)


@pytest.mark.parametrize("test_values", type_probabilities_positive_test_data)
def test_set_type_probabilities_positive(test_values):
    test_class = EquationGenerator()
    test_class.set_type_probabilities(test_values)
    configured_values = test_class.get_type_probabilities()
    assert configured_values == test_values


@pytest.mark.parametrize("test_values", type_probabilities_negative_test_data)
def test_set_type_probabilities_negative(test_values):
    test_class = EquationGenerator()
    with pytest.raises(Exception):
        test_class.set_type_probabilities(test_values)


@pytest.mark.parametrize("test_values", oper_probabilities_positive_test_data)
def test_set_operation_probabilities_positive(test_values):
    test_class = EquationGenerator()
    test_class.set_operation_probabilities(test_values)
    configured_values = test_class.get_operation_probabilities()
    assert configured_values == test_values


@pytest.mark.parametrize("test_values", oper_probabilities_negative_test_data)
def test_set_operation_probabilities_negative(test_values):
    test_class = EquationGenerator()
    with pytest.raises(Exception):
        test_class.set_operation_probabilities(test_values)


@pytest.mark.parametrize("test_values", oper_operands_positive_test_data)
def test_set_operation_operands_positive(test_values):
    test_class = EquationGenerator()
    test_class.set_operation_operands(test_values)
    configured_values = test_class.get_operation_operands()
    assert configured_values == test_values


@pytest.mark.parametrize("test_value", expression_probability_positive_test_data)
def test_set_expression_probabilities_positive(test_value):
    test_class = EquationGenerator()
    test_class.set_expression_probability(test_value)
    configured_value = test_class.get_expression_probability()
    assert configured_value == test_value


@pytest.mark.parametrize("test_value", expression_probability_negative_test_data)
def test_set_expression_probabilities_negative(test_value):
    test_class = EquationGenerator()
    with pytest.raises(Exception):
        test_class.set_expression_probability(test_value)


@pytest.mark.parametrize("oper_operands, oper_probabilities, values_num, type_ranges, type_probabilities,\
                         expression_probability, expected",
                         generate_equation_positive_test_data)
def test_generate_equation_positive(oper_operands,
                                    oper_probabilities,
                                    values_num,
                                    type_ranges,
                                    type_probabilities,
                                    expression_probability,
                                    expected):
    test_class = EquationGenerator()
    test_class.set_operation_operands(oper_operands)
    test_class.set_operation_probabilities(oper_probabilities)
    test_class.set_values_num(values_num)
    test_class.set_type_ranges(type_ranges)
    test_class.set_type_probabilities(type_probabilities)
    test_class.set_expression_probability(expression_probability)
    test_class.generate_equation()
    equation = test_class.get_equation()
    assert equation == expected
