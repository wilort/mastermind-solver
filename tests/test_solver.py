from src.solver import MastermindSolver
from src.mastermind import Mastermind, Colors
from unittest import mock
from pytest import fixture
import pytest
import time

@fixture
def mastermind():
    mocked_solution = [Colors.RED, Colors.BLUE, Colors.GREEN, Colors.YELLOW]
    with mock.patch("random.choices", return_value=mocked_solution):
    #with mock.patch("random.sample", return_value=mocked_solution):
        mastermind = Mastermind()
        mastermind.new_game()
        return mastermind

def test_solver_with_correct_first_guess(mastermind):

    mastermind.set_solution([Colors.RED, Colors.BLUE, Colors.GREEN, Colors.YELLOW])

    mocked_first_guess = [Colors.RED, Colors.BLUE, Colors.GREEN, Colors.YELLOW]

    solver = MastermindSolver(mastermind)

    with mock.patch.object(MastermindSolver, "create_guess", return_value=mocked_first_guess):
        solution, num_iterations = solver.solve()
        assert mastermind.check_solution(solution)
        assert num_iterations == 0

@pytest.mark.parametrize("mocked_first_guess, expected_iterations", [
    ([Colors.RED, Colors.BLUE, Colors.GREEN, Colors.BLACK], 2),
    ([Colors.RED, Colors.BLUE, Colors.GREEN, Colors.ORANGE], 1),
    ([Colors.BLACK, Colors.BLUE, Colors.YELLOW, Colors.ORANGE], 5),
])
def test_solver_with_guess(mastermind, mocked_first_guess, expected_iterations):

    mastermind.set_solution([Colors.RED, Colors.BLUE, Colors.GREEN, Colors.YELLOW])

    solver = MastermindSolver(mastermind)

    with mock.patch.object(MastermindSolver, "create_guess", return_value=mocked_first_guess):
        solution, num_iterations = solver.solve()
        assert mastermind.check_solution(solution)
        assert num_iterations == expected_iterations

def test_solver_no_balls_in_guess(mastermind):

    mastermind.set_solution([Colors.RED, Colors.BLUE, Colors.GREEN, Colors.YELLOW])

    solver = MastermindSolver(mastermind)

    mocked_first_guess = [Colors.ORANGE, Colors.BROWN, Colors.WHITE, Colors.BLACK]

    with mock.patch.object(MastermindSolver, "create_guess", return_value=mocked_first_guess):
        solution, num_iterations = solver.solve()
        assert mastermind.check_solution(solution)
        assert num_iterations == 4

def test_solver(mastermind):

    solver = MastermindSolver(mastermind)

    solution, num_iterations = solver.solve()
    assert mastermind.check_solution(solution)
    assert num_iterations <= 6

def test_solver_timing():

    accumulated_cpu_time = 0
    mastermind = Mastermind()
    solver = MastermindSolver(mastermind)

    for _ in range(100):
        solver.mastermind.new_game()
        start_time = time.process_time()
        solution, num_iterations = solver.solve(write_lp_file=False)
        end_time = time.process_time()
        accumulated_cpu_time += end_time - start_time
        assert mastermind.check_solution(solution)
    assert 0.6 < accumulated_cpu_time
    assert accumulated_cpu_time < 0.7