from src.solver import MastermindSolver
from src.mastermind import Mastermind, Colors
from unittest import mock
from pytest import fixture
import pytest
import time
import random
from itertools import product

@fixture
def mastermind():
    # mocked_solution = [Colors.RED, Colors.BLUE, Colors.GREEN, Colors.YELLOW]
    # with mock.patch("random.choices", return_value=mocked_solution):
    # #with mock.patch("random.sample", return_value=mocked_solution):
    #     mastermind = Mastermind()
    #     mastermind.new_game()
    #     return mastermind
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
    ([Colors.RED, Colors.BLUE, Colors.GREEN, Colors.ORANGE], 2),
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

    random.seed(42)
    solver = MastermindSolver(mastermind)

    solution, num_iterations = solver.solve(write_lp_file=True)
    assert mastermind.check_solution(solution)
    assert num_iterations <= 5

def atest_solver_timing():

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

def test_solver_num_iterations():

    mastermind = Mastermind()
    solver = MastermindSolver(mastermind)
    random.seed(42)

    num_simulations = 100
    total_num_iterations = 0
    max_num_iterations = 0
    for _ in range(num_simulations):
        solver.mastermind.new_game()
        solution, num_iterations = solver.solve(write_lp_file=False)
        total_num_iterations += num_iterations
        max_num_iterations = max(max_num_iterations, num_iterations)
        assert mastermind.check_solution(solution)
    assert total_num_iterations == 372
    assert max_num_iterations == 6

def generate_random_solution_with_duplicates():
    colors = list(Colors)
    solution = random.choices(colors, k=4)
    if len(set(solution)) == len(solution):
        solution[-1] = solution[0]
    return solution

def test_solver_num_iterations_with_duplicates():

    mastermind = Mastermind(allow_duplicates=True)
    solver = MastermindSolver(mastermind)
    random.seed(42)

    num_simulations = 100
    total_num_iterations = 0
    max_num_iterations = 0
    for _ in range(num_simulations):
        my_solution = generate_random_solution_with_duplicates()
        solver.mastermind.set_solution(my_solution)
        solution, num_iterations = solver.solve()
        total_num_iterations += num_iterations
        max_num_iterations = max(max_num_iterations, num_iterations)
        assert mastermind.check_solution(solution)
    assert total_num_iterations == 481
    assert max_num_iterations == 7


def test_solver_all_color_combinations():

    random.seed(42)

    mastermind = Mastermind(allow_duplicates=True)

    solver = MastermindSolver(mastermind)
    
    total_num_iterations = 0
    max_num_iterations = 0

    for code in product(Colors, repeat=4):
        solver.mastermind.set_solution(list(code))
        solution, num_iterations = solver.solve()
        assert mastermind.check_solution(solution)
        total_num_iterations += num_iterations
        max_num_iterations = max(max_num_iterations, num_iterations)
    assert total_num_iterations == 20318
    assert max_num_iterations == 11
