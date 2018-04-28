import pytest

from QTemplate.solver.operand_solver import OperandSolver


@pytest.mark.parametrize('ops, empty, paren, expected', [
    ({'+'}, False, False, {'+'}),
    ({'+'}, True, False, {'+', ''}),
    ({'+'}, False, True, {'+'}),
    ({'*'}, True, True, {'*', ''}),
    (None, False, False, {'+', '-', '*', '/'}),
    (None, True, False, {'+', '-', '*', '/', ''}),
])
def test_ops_initialization(ops, empty, paren, expected):
    op_solver = OperandSolver(numbers=[1, 2],
                              target=3,
                              ops=ops,
                              allow_empty=empty,
                              use_parenthesis=paren)
    assert op_solver.ops == expected


def test_initialization_fail_with_no_data():
    with pytest.raises(Exception):
        OperandSolver()


@pytest.mark.parametrize('numbers, target', [
    (1, 1),
    ([1, 2], None),
])
def test_initialization_fail_with_wrong_data(numbers, target):
    with pytest.raises(Exception):
        OperandSolver(numbers=numbers, target=target)


@pytest.mark.parametrize('test_input, expected', [
    ('6', '{}6{}'),
    ('1+2', '{}1{}+{}2{}'),
    ('1+2-3', '{}1{}+{}2{}-{}3{}')
])
def test_add_curly_brace_to_one(test_input, expected):
    assert OperandSolver._add_curly_brace_to_one(test_input) == expected


@pytest.mark.parametrize('test_input, expected', [
    ([1, 2, 3], ['1', '2', '3']),
    (['1', 2, 3], ['1', '2', '3'])
])
def test_convert_data(test_input, expected):
    assert OperandSolver._convert_data(test_input) == expected


def test_convert_data_fail():
    with pytest.raises(Exception):
        OperandSolver._convert_data({1: 2})


@pytest.mark.parametrize('test_input, expected', [
    ('(1+2)', True),
    ('(1)+2', False),
    ('1+2', True),
    ('()', False),
    ('(45-(20)+8)', False)
])
def test_single_number_validation(test_input, expected):
    assert OperandSolver._single_number_validation(test_input) == expected


@pytest.mark.parametrize('expr, expected', [
    ('(1+2)', True),
    ('1+(2+3)', True),
    ('(1+(2+3)+4)', False),
    ('1+2+2', True),
    ('(1+(2)', False),
    ('(1+2))', False)
])
def test_parenthesis_number_validation(expr, expected):
    assert OperandSolver._parenthesis_number_validation(expr) == expected


@pytest.mark.parametrize('expr, expected', [
    (')1(', False),
    (')1', False),
    ('1(', False),
    ('(1+2)', True)
])
def test_parenthesis_validation(expr, expected):
    assert OperandSolver._parenthesis_validation(expr) == expected


@pytest.mark.parametrize('formula, ops, target, expected', [
    ('1{}2', {'+', '-', ''}, 3, {'1+2'}),
    ('1{}2{}3', {'+', '-', ''}, 9, {'12-3'}),
])
def test_solver_wo_parenthesis(formula, ops, target, expected):
    result = OperandSolver._solver_wo_parenthesis(formula, ops, target)
    assert result == expected


@pytest.mark.parametrize('formula, target, expected', [
    ('{}1{}+{}2{}+{}3{}', 6, {'(1+2)+3', '1+(2+3)', '(1+2+3)'}),
    ('{}1{}+{}2{}+{}3{}+{}4{}', 10, {'(1+2+3+4)', '(1+2)+3+4', '(1+2+3)+4',
                                     '1+(2+3)+4', '1+(2+3+4)', '1+2+(3+4)'})
])
def test_solver_for_parenthesis(formula, target, expected):
    assert OperandSolver._solver_for_parenthesis(formula, target) == expected


@pytest.mark.parametrize('numbers, target, ops, empty, paren, expected', [
    ([1, 2, 3], 6, None, False, False, {'1+2+3', '1*2*3'}),
    ([1, 2, 3], 15, {'+', '-'}, True, False, {'12+3'}),
    ([1, 2, 3], 9, {'+', '-'}, False, False, set()),
    ([1, 2, 3], 9, {'+', '-'}, True, False, {'12-3'}),
    ([1, 2], 3, {'+', '-'}, True, True, {'1+2', '(1+2)'}),
    ([1, 2, 3], 6, {'+', '-'}, True, True, {'1+2+3', '(1+2)+3',
                                            '1+(2+3)', '(1+2+3)'}),
    ([1, 2, 3, 4], 10, {'+', '-'}, True, True, {'1+2+3+4', '(1+2+3+4)',
                                                '(1+2)+3+4', '(1+2+3)+4',
                                                '1+(2+3)+4', '1+(2+3+4)',
                                                '1+2+(3+4)'}),
    ([1, 2, 3], 9, None, False, False, set()),
    ([1, 2, 3], 9, None, False, True, {'(1+2)*3'}),
    ([2, 2, 3], 12, None, False, False, {'2*2*3'}),
    ([2, 4, 2], 4, None, False, False, {'2*4/2', '2+4-2', '2+4/2'}),
])
def test_solve(numbers, target, ops, empty, paren, expected):
    op_solver = OperandSolver(numbers=numbers,
                              target=target,
                              ops=ops,
                              allow_empty=empty,
                              use_parenthesis=paren)
    assert op_solver.solve() == expected


@pytest.mark.parametrize('sign_list, expected', [
    (['-', '(', '-', ')'], ['-', '(', '+', ')']),
    (['-', '(', '+', ')'], ['-', '(', '-', ')']),
    (['/', '(', '*', ')'], ['/', '(', '/', ')']),
    (['/', '(', '/', ')'], ['/', '(', '*', ')']),
])
def test_fix_sign(sign_list, expected):
    assert OperandSolver._fix_sign(sign_list) == expected
