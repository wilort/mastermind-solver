from src.mastermind import Mastermind
from src.mastermind import Colors as C
from src.mastermind import PegColors as PC
from unittest import mock
from pytest import fixture
import pytest

@fixture
def mastermind():
    mocked_solution = [C.RED, C.BLUE, C.GREEN, C.YELLOW]
    with mock.patch("random.choices", return_value=mocked_solution):
        mastermind = Mastermind()
        mastermind.new_game()
        return mastermind

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

def atest_get_hint(mastermind):

    mastermind.set_solution([C.RED, C.BLUE, C.GREEN, C.YELLOW])

    guess = [C.YELLOW, C.ORANGE, C.GREEN, C.BLACK]
    hint = mastermind.get_hint(guess)

    assert PC.RED in hint
    assert hint.count(PC.RED) == 1

@pytest.mark.parametrize("guess, expected_hint", [
    ([C.RED, C.BLUE, C.GREEN, C.YELLOW], [PC.RED, PC.RED, PC.RED, PC.RED]),
    ([C.BLUE, C.RED, C.YELLOW, C.GREEN], [PC.WHITE, PC.WHITE, PC.WHITE, PC.WHITE]),
    ([C.ORANGE, C.BROWN, C.WHITE, C.BLACK], [PC.NONE, PC.NONE, PC.NONE, PC.NONE]),
    ([C.RED, C.GREEN, C.BLUE, C.BLACK], [PC.RED, PC.WHITE, PC.WHITE, PC.NONE]),
    ([C.RED, C.RED, C.RED, C.RED], [PC.RED, PC.WHITE, PC.WHITE, PC.WHITE]),
    ([C.BLUE, C.RED, C.YELLOW, C.BLACK], [PC.WHITE, PC.WHITE, PC.WHITE, PC.NONE]),
])
def test_get_hint(mastermind, guess, expected_hint):

    solution = [C.RED, C.BLUE, C.GREEN, C.YELLOW]

    mastermind.set_solution(solution)

    hint = mastermind.get_hint(guess)

    for pc in list(PC):
        assert hint.count(pc) == expected_hint.count(pc)