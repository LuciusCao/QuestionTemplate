import pytest

from QTemplate.solver.solver import Solver


def test_initialization():
    solver = Solver(None, None)
    assert solver.content is None
    assert solver.config is None


def test_empty_initialization():
    solver = Solver()
    assert solver.content is None
    assert solver.config is None


def test_solve():
    solver = Solver()
    assert solver.solve() == set()
