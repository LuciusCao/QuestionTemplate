import pytest

from QTemplate.solver.match_game_solver import MatchGameSolver


@pytest.mark.parametrize('question, expected', [
    ('1+2=3', ['1', '+', '2', '3']),
    ('1-2-2=3', ['1', '-', '2', '-', '2', '3'])
])
def test_extract_numbers_from_questions(question, expected):
    assert MatchGameSolver._extract_numbers_from_question(question) == expected


@pytest.mark.parametrize('question, expected', [
    ('1+2=3', '{}{}{}={}'),
    ('1-2-2=3', '{}{}{}{}{}={}')
])
def test_replace_with_curly_brace(question, expected):
    assert MatchGameSolver._replace_with_curly_brace(question) == expected


@pytest.mark.parametrize('question, expected', [
    ('1+2=3', ['1+2', '3']),
    ('1=3-2', ['1', '3-2'])
])
def test_get_question_and_key(question, expected):
    assert MatchGameSolver._get_question_and_key(question) == expected


@pytest.mark.parametrize('question, num_moves, mode, expected', [
    ('1+4=11', 1, '+', {'7+4=11'}),
    ('15=1+0', 1, '+', {'15=7+8'})
])
def test_solve_for_add_one(question, num_moves, mode, expected):
    match_game_solver = MatchGameSolver(question, num_moves, mode)
    match_game_solver._solve_for_add_one(question)
