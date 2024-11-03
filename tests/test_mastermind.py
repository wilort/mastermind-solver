from src.mastermind import Mastermind
from src.mastermind import Colors as C
from src.mastermind import PegColors as PC
import pytest

def test_set_solution():
    mastermind = Mastermind(allow_duplicates=False)
    solution = [C.RED, C.BLUE, C.GREEN, C.YELLOW]
    mastermind.set_solution(solution)
    assert mastermind.solution == solution

def test_set_solution_with_duplicates():
    mastermind = Mastermind(allow_duplicates=True)
    solution = [C.RED, C.RED, C.GREEN, C.YELLOW]
    mastermind.set_solution(solution)
    assert mastermind.solution == solution

def test_set_solution_with_duplicates_error():
    mastermind = Mastermind(allow_duplicates=False)
    solution = [C.RED, C.RED, C.GREEN, C.YELLOW]
    with pytest.raises(ValueError):
        mastermind.set_solution(solution)

@pytest.mark.parametrize("solution, guess, expected_hint", [
    ([C.BLUE, C.GREEN, C.YELLOW, C.BLACK],  [C.GREEN, C.RED, C.GREEN, C.BLACK],     [PC.RED, PC.WHITE, PC.NONE, PC.NONE]),
    ([C.BLUE, C.GREEN, C.YELLOW, C.BLACK],  [C.GREEN, C.GREEN, C.BLUE, C.WHITE],    [PC.RED, PC.WHITE, PC.NONE, PC.NONE]),
    ([C.BLUE, C.GREEN, C.YELLOW, C.BLACK],  [C.GREEN, C.BLACK, C.WHITE, C.YELLOW],  [PC.WHITE, PC.WHITE, PC.WHITE, PC.NONE]),
    ([C.BLUE, C.GREEN, C.YELLOW, C.BLACK],  [C.WHITE, C.GREEN, C.WHITE, C.BLACK],   [PC.RED, PC.RED, PC.NONE, PC.NONE]),
    ([C.BLUE, C.GREEN, C.YELLOW, C.BLACK],  [C.YELLOW, C.GREEN, C.YELLOW, C.BLACK], [PC.RED, PC.RED, PC.RED, PC.NONE]),
    ([C.BLUE, C.GREEN, C.YELLOW, C.BLACK],  [C.BLUE, C.GREEN, C.YELLOW, C.BLACK],   [PC.RED, PC.RED, PC.RED, PC.RED]),
    ([C.RED, C.BLUE, C.RED, C.BLUE],        [C.BLUE, C.RED, C.BLUE, C.RED],         [PC.WHITE, PC.WHITE, PC.WHITE, PC.WHITE]),
    ([C.RED, C.BLUE, C.RED, C.BLUE],        [C.RED, C.BLUE, C.BLUE, C.RED],         [PC.RED, PC.RED, PC.WHITE, PC.WHITE]),
    ([C.RED, C.RED, C.BLUE, C.BLUE],        [C.RED, C.RED, C.RED, C.BLUE],          [PC.RED, PC.RED, PC.RED, PC.NONE]),
    ([C.BLUE, C.GREEN, C.YELLOW, C.BLACK],  [C.GREEN, C.RED, C.GREEN, C.BLACK],     [PC.RED, PC.WHITE, PC.NONE, PC.NONE]),
    ([C.YELLOW, C.YELLOW, C.GREEN, C.BLUE], [C.YELLOW, C.BLUE, C.GREEN, C.BLACK],   [PC.RED, PC.RED, PC.WHITE, PC.NONE]),
    ([C.RED, C.BLUE, C.GREEN, C.YELLOW],    [C.RED, C.BLUE, C.GREEN, C.YELLOW],     [PC.RED, PC.RED, PC.RED, PC.RED]),
    ([C.RED, C.BLUE, C.GREEN, C.YELLOW],    [C.BLUE, C.RED, C.YELLOW, C.GREEN],     [PC.WHITE, PC.WHITE, PC.WHITE, PC.WHITE]),
    ([C.RED, C.BLUE, C.GREEN, C.YELLOW],    [C.WHITE, C.BLACK, C.WHITE, C.BLACK],   [PC.NONE, PC.NONE, PC.NONE, PC.NONE]),
    ([C.RED, C.BLUE, C.GREEN, C.YELLOW],    [C.RED, C.GREEN, C.BLUE, C.BLACK],      [PC.RED, PC.WHITE, PC.WHITE, PC.NONE]),
    ([C.RED, C.BLUE, C.GREEN, C.YELLOW],    [C.RED, C.RED, C.RED, C.RED],           [PC.RED, PC.NONE, PC.NONE, PC.NONE]),
    ([C.RED, C.BLUE, C.GREEN, C.YELLOW],    [C.BLUE, C.RED, C.YELLOW, C.BLACK],     [PC.WHITE, PC.WHITE, PC.WHITE, PC.NONE]),
])
def test_get_hint(solution, guess, expected_hint):

    mastermind = Mastermind(allow_duplicates=True)

    mastermind.set_solution(solution)

    hint = mastermind.get_hint(guess)

    for pc in list(PC):
        assert hint.count(pc) == expected_hint.count(pc)