import pytest

from QTemplate.solver.operand_solver import OperandSolver


@pytest.mark.parametrize('test_input, expected', [
    ((False, False), ['+', '-']),
    ((True, False), ['+', '-', '']),
])
def test_initialization(test_input, expected):
    op_solver = OperandSolver(formula=0,
                              target=0,
                              allow_empty=test_input[0],
                              use_parenthesis=test_input[1])
    assert op_solver.operand == expected

def test_initialization_fail():
    with pytest.raises(Exception):
        OperandSolver()


@pytest.mark.parametrize('test_input, expected', [
    (15, ['15']),
    ([1, 2, 3], ['1', '2', '3']),
    (['1', 2, 3], ['1', '2', '3'])
])
def test_convert_data(test_input, expected):
    assert OperandSolver._convert_data(test_input) == expected


def test_convert_data_fail():
    with pytest.raises(Exception):
        OperandSolver._convert_data({1:2})


@pytest.mark.parametrize('test_input, expected', [
    ((6, 6, False, False), [[]]),
    (([1, 2, 3], 6, False, False), [['+', '+']]),
    (([1, 2, 3], 15, True, False), [['', '+']]),
    (([1, 2, 3], 9, False, False), []),
    (([1, 2, 3], 9, True, True), [['', '-']])
])
def test_solve(test_input, expected):
    op_solver = OperandSolver(formula=test_input[0],
                              target=test_input[1],
                              allow_empty=test_input[2],
                              use_parenthesis=test_input[3])
    assert op_solver.solve() == expected
