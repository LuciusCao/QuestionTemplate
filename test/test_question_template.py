import pytest
from QTemplate.question_template import QuestionTemplate


@pytest.mark.parametrize('test_input, expected', [
    ('<a>+<b>', '{}+{}'),
    ('<a><<b>', '{}<{}'),
    ('<a>><b>', '{}>{}'),
    ('<b>', '{}'),
    ('', ''),
    ('this is a dummy test', 'this is a dummy test')
])
def test_parse_template(test_input, expected):
    assert QuestionTemplate._parse_template(test_input) == expected


@pytest.mark.parametrize('test_input, expected', [
    ('text <a+b>, good <a*b>.', ['a+b', 'a*b']),
    ('text <a+b> < <x/y> good', ['a+b', 'x/y']),
    ('text <a+b> > <x/y> good', ['a+b', 'x/y']),
    ('<a>', ['a']),
    ('', []),
    ('this is a dummy test', [])
])
def test_parse_expressions(test_input, expected):
    assert QuestionTemplate._parse_expressions(test_input) == expected


@pytest.mark.parametrize('test_input, random_state, expected', [
    ('int from 10 to 30', 1, 14),
    ('float from 10 to 30', 1, 12.687284882248024)
])
def test_parse_rule(test_input, random_state, expected):
    output = QuestionTemplate._parse_rule(test_input, random_state=random_state)
    assert  output == pytest.approx(expected)
