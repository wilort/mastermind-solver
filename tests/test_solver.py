from src.solver import MastermindSolver
from src.mastermind import Mastermind, Colors
from unittest import mock
from pytest import fixture

@fixture
def mastermind():
    mocked_solution = [Colors.RED, Colors.BLUE, Colors.GREEN, Colors.YELLOW]
    with mock.patch("random.choices", return_value=mocked_solution):
        mastermind = Mastermind()
        mastermind.new_game()
        return mastermind

def test_solver(mastermind):
    solver = MastermindSolver(mastermind)
    solution, num_iterations = solver.solve()
    assert len(solution) == mastermind.code_length
    assert solution == mastermind.solution

