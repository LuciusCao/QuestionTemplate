import pytest

from QTemplate.solver.operand_solver import OperandSolver


@pytest.mark.parametrize('test_input, expected', [
    ((False, False), {'+', '-'}),
    ((True, False), {'+', '-', ''}),
])
def test_initialization(test_input, expected):
    op_solver = OperandSolver(numbers=[1, 2],
                              target=3,
                              allow_empty=test_input[0],
                              use_parenthesis=test_input[1])
    assert op_solver.operands == expected


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
    ('()', False)
])
def test_expr_validation(test_input, expected):
    assert OperandSolver._expr_validation(test_input) == expected


@pytest.mark.parametrize('formula, ops, target, expected', [
    ('1{}2', {'+', '-', ''}, 3, {'1+2'}),
    ('1{}2{}3', {'+', '-', ''}, 9, {'12-3'}),
    ('{}1{}+{}2{}+{}3{}', {'(', ')', ''}, 6, {'1+2+3', '(1+2)+3',
                                              '1+(2+3)', '(1+2+3)'})
])
def test_solver(formula, ops, target, expected):
    assert OperandSolver._solver(formula, ops, target) == expected


@pytest.mark.parametrize('test_input, expected', [
    (([1, 2, 3], 6, False, False), {'1+2+3'}),
    (([1, 2, 3], 15, True, False), {'12+3'}),
    (([1, 2, 3], 9, False, False), set()),
    (([1, 2, 3], 9, True, False), {'12-3'}),
    (([1, 2], 3, True, True), {'1+2', '(1+2)'})
])
def test_solve(test_input, expected):
    op_solver = OperandSolver(numbers=test_input[0],
                              target=test_input[1],
                              allow_empty=test_input[2],
                              use_parenthesis=test_input[3])
    assert op_solver.solve() == expected
