import pytest

from QTemplate.solver.match_game_solver import MatchGameSolver


@pytest.mark.parametrize('question, expected', [
    ('1+2=3', ['1', '+', '2', '3']),
    ('1-2-2=3', ['1', '-', '2', '-', '2', '3']),
    ('15=7+0', ['1', '5', '7', '+', '0'])
])
def test_extract_numbers_from_questions(question, expected):
    assert MatchGameSolver._extract_numbers(question) == expected


@pytest.mark.parametrize('question, expected', [
    ('1+2=3', '{}{}{}={}'),
    ('1-2-2=3', '{}{}{}{}{}={}'),
    ('15=7+0', '{}{}={}{}{}')
])
def test_replace_with_curly_brace(question, expected):
    assert MatchGameSolver._replace_with_curly_brace(question) == expected


@pytest.mark.parametrize('expression, expected', [
    ('1+2=4', False),
    ('100-2+101=199', True),
    ('100 - 2 = 98', True)
])
def test_judge_expression(expression, expected):
    assert MatchGameSolver._judge_expression(expression) == expected


@pytest.mark.parametrize('question, num_moves, mode, expected', [
    ('1+4=11', 1, '+', {'7+4=11'}),
    ('15=7+0', 1, '+', {'15=7+8'}),
    ('7+0=15', 1, '+', {'7+8=15'}),
    ('3+1=10', 1, '+', {'9+1=10', '3+7=10'}),
    ('7+8=7', 1, '-', {'7+0=7'}),
    ('9+8=1', 1, '-', {'9-8=1'})
])
def test_solve(question, num_moves, mode, expected):
    match_game_solver = MatchGameSolver(question, num_moves, mode)
    assert match_game_solver.solve() == expected
