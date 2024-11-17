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
        assert num_iterations == 1

@pytest.mark.parametrize("mocked_first_guess, expected_iterations", [
    ([Colors.RED, Colors.BLUE, Colors.GREEN, Colors.BLACK], 3),
    ([Colors.BLACK, Colors.BLUE, Colors.YELLOW, Colors.RED], 4),
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

    mocked_first_guess = [Colors.WHITE, Colors.BLACK, Colors.WHITE, Colors.BLACK]

    with mock.patch.object(MastermindSolver, "create_guess", return_value=mocked_first_guess):
        solution, num_iterations = solver.solve()
        assert mastermind.check_solution(solution)
        assert num_iterations == 4

def test_solver_one_color_solution(mastermind):

    mastermind.allow_duplicates = True

    mastermind.set_solution([Colors.RED, Colors.RED, Colors.RED, Colors.RED])

    solver = MastermindSolver(mastermind)

    mocked_first_guess = [Colors.RED, Colors.RED, Colors.RED, Colors.BLUE]

    with mock.patch.object(MastermindSolver, "create_guess", return_value=mocked_first_guess):
        solution, num_iterations = solver.solve(write_lp_file=True)
        assert mastermind.check_solution(solution)
        assert num_iterations == 2

def test_solver_all_color_combinations():

    mastermind = Mastermind(allow_duplicates=True)

    solver = MastermindSolver(mastermind)
    
    iterations = {i: 0 for i in range(1, 11)}

    for code in product(Colors, repeat=4):
        solver.mastermind.set_solution(list(code))
        solution, num_iterations = solver.solve()
        assert mastermind.check_solution(solution)
        iterations[num_iterations] += 1

    expected_iterations = {
        1: 1,
        2: 13,
        3: 57,
        4: 195,
        5: 348,
        6: 357,
        7: 229,
        8: 79,
        9: 17,
        10: 0
    }

    total_num_iterations = sum(k*v for k, v in iterations.items())

    assert total_num_iterations == 7248
    assert iterations == expected_iterations

# Solution: [<Colors.WHITE: 'WHITE'>, <Colors.WHITE: 'WHITE'>, <Colors.WHITE: 'WHITE'>, <Colors.BLUE: 'BLUE'>]
# guess_1: [<Colors.RED: 'RED'>, <Colors.BLUE: 'BLUE'>, <Colors.GREEN: 'GREEN'>, <Colors.YELLOW: 'YELLOW'>]
# hint_1: [<PegColors.NONE: 'NONE'>, <PegColors.WHITE: 'WHITE'>, <PegColors.NONE: 'NONE'>, <PegColors.NONE: 'NONE'>]
# guess_2: [<Colors.WHITE: 'WHITE'>, <Colors.BLACK: 'BLACK'>, <Colors.RED: 'RED'>, <Colors.BLACK: 'BLACK'>]
# hint_2: [<PegColors.NONE: 'NONE'>, <PegColors.NONE: 'NONE'>, <PegColors.RED: 'RED'>, <PegColors.NONE: 'NONE'>]
# guess_3: [<Colors.BLUE: 'BLUE'>, <Colors.RED: 'RED'>, <Colors.RED: 'RED'>, <Colors.GREEN: 'GREEN'>]
# hint_3: [<PegColors.NONE: 'NONE'>, <PegColors.NONE: 'NONE'>, <PegColors.WHITE: 'WHITE'>, <PegColors.NONE: 'NONE'>]
# guess_4: [<Colors.WHITE: 'WHITE'>, <Colors.WHITE: 'WHITE'>, <Colors.BLUE: 'BLUE'>, <Colors.BLUE: 'BLUE'>]
# hint_4: [<PegColors.RED: 'RED'>, <PegColors.RED: 'RED'>, <PegColors.RED: 'RED'>, <PegColors.NONE: 'NONE'>]
# guess_5: [<Colors.WHITE: 'WHITE'>, <Colors.WHITE: 'WHITE'>, <Colors.BLUE: 'BLUE'>, <Colors.WHITE: 'WHITE'>]
# hint_5: [<PegColors.RED: 'RED'>, <PegColors.WHITE: 'WHITE'>, <PegColors.WHITE: 'WHITE'>, <PegColors.RED: 'RED'>]
# guess_6: [<Colors.WHITE: 'WHITE'>, <Colors.YELLOW: 'YELLOW'>, <Colors.BLUE: 'BLUE'>, <Colors.BLUE: 'BLUE'>]
# hint_6: [<PegColors.NONE: 'NONE'>, <PegColors.RED: 'RED'>, <PegColors.NONE: 'NONE'>, <PegColors.RED: 'RED'>]
# guess_7: [<Colors.WHITE: 'WHITE'>, <Colors.WHITE: 'WHITE'>, <Colors.BLACK: 'BLACK'>, <Colors.BLUE: 'BLUE'>]
# hint_7: [<PegColors.RED: 'RED'>, <PegColors.NONE: 'NONE'>, <PegColors.RED: 'RED'>, <PegColors.RED: 'RED'>]
# guess_8: [<Colors.WHITE: 'WHITE'>, <Colors.WHITE: 'WHITE'>, <Colors.YELLOW: 'YELLOW'>, <Colors.BLUE: 'BLUE'>]
# hint_8: [<PegColors.RED: 'RED'>, <PegColors.NONE: 'NONE'>, <PegColors.RED: 'RED'>, <PegColors.RED: 'RED'>]
# guess_9: [<Colors.WHITE: 'WHITE'>, <Colors.WHITE: 'WHITE'>, <Colors.WHITE: 'WHITE'>, <Colors.BLUE: 'BLUE'>]
# hint_9: [<PegColors.RED: 'RED'>, <PegColors.RED: 'RED'>, <PegColors.RED: 'RED'>, <PegColors.RED: 'RED'>]

def test_solver_many_iterations_example():

    mastermind = Mastermind(allow_duplicates=True)

    mastermind.set_solution([Colors.WHITE, Colors.WHITE, Colors.WHITE, Colors.BLUE])

    solver = MastermindSolver(mastermind)

    solution, num_iterations = solver.solve()

    assert mastermind.check_solution(solution)

    assert num_iterations == 9