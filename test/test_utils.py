import pytest


from QTemplate.utils import (
    extract_var_expressions,
    parse_template,
    get_expressions_to_eval,
    evaluate_expressions,
    inject_data_to_template,
)


@pytest.mark.parametrize('test_input, expected', [
    ('<a>+<b>', '{}+{}'),
    ('<a><<b>', '{}<{}'),
    ('<a>><b>', '{}>{}'),
    ('<b>', '{}'),
    ('', ''),
    ('this is a dummy test', 'this is a dummy test')
])
def test_parse_template(test_input, expected):
    assert parse_template(test_input) == expected


@pytest.mark.parametrize('test_input, expected', [
    ('text <a+b>, good <a*b>.', ['a+b', 'a*b']),
    ('text <a+b> < <x/y> good', ['a+b', 'x/y']),
    ('text <a+b> > <x/y> good', ['a+b', 'x/y']),
    ('<a>', ['a']),
    ('', []),
    ('this is a dummy test', [])
])
def test_extract_var_expressions(test_input, expected):
    assert extract_var_expressions(test_input) == expected


@pytest.mark.parametrize('var_dict, exprs, expected', [
    ({'a': 6}, ['a+1'], ['6+1']),
    ({'a': 6, 'b': 7}, ['a+b', 'a*b'], ['6+7', '6*7']),
    (dict(), ['a+b', '1+7'], ['a+b', '1+7']),
    ({'a': 2}, ['a+b'], ['2+b']),
])
def test_get_expressions_to_eval(var_dict, exprs, expected):
    assert get_expressions_to_eval(var_dict, exprs) == expected


@pytest.mark.parametrize('exprs, expected', [
    (['1+7', '2+9'], [8, 11]),
    ([], []),
    (['a+b', '3+3'], [-1, -1]),
])
def test_evaluate_expressions(exprs, expected):
    assert evaluate_expressions(exprs) == expected

@pytest.mark.parametrize('template, data, expected', [
    ('', [], ''),
    ('{}-{}', [], '-1--1'),
    ('{}-{}', [1, 2], '1-2'),
    ('{}+{}', [2,], '-1+-1'),
    ('{}', [1, 2, 3], '1'),
])
def test_inject_data_to_template(template, data, expected):
    assert inject_data_to_template(template, data) == expected
