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

def test_solver_correct_first_guess(mastermind):

    solver = MastermindSolver(mastermind)

    mocked_first_guess = [Colors.RED, Colors.BLUE, Colors.GREEN, Colors.YELLOW]

    with mock.patch.object(MastermindSolver, "create_guess", return_value=mocked_first_guess):
        solution, num_iterations = solver.solve()
        assert mastermind.check_solution(solution)

def test_solver_incorrect_first_guess(mastermind):

    solver = MastermindSolver(mastermind)

    mocked_first_guess = [Colors.RED, Colors.BLUE, Colors.GREEN, Colors.ORANGE]

    with mock.patch.object(MastermindSolver, "create_guess", return_value=mocked_first_guess):
        solution, num_iterations = solver.solve()
        assert mastermind.check_solution(solution)

def test_solver(mastermind):

    solver = MastermindSolver(mastermind)

    solution, num_iterations = solver.solve()
    assert mastermind.check_solution(solution)