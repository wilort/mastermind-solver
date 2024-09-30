from src.mastermind import Mastermind, Colors, PegColors
from unittest import mock
from pytest import fixture
import pytest

@fixture
def mastermind():
    mocked_solution = [Colors.RED, Colors.BLUE, Colors.GREEN, Colors.YELLOW]
    with mock.patch("random.choices", return_value=mocked_solution):
        mastermind = Mastermind()
        mastermind.new_game()
        return mastermind

def test_get_hint(mastermind):

    mastermind.set_solution([Colors.RED, Colors.BLUE, Colors.GREEN, Colors.YELLOW])

    guess = [Colors.YELLOW, Colors.ORANGE, Colors.GREEN, Colors.BLACK]
    hint = mastermind.get_hint(guess)

    assert PegColors.RED in hint
    assert hint.count(PegColors.RED) == 1

def test_mastermind_incorrect_guess(mastermind):

    mastermind.set_solution([Colors.RED, Colors.BLUE, Colors.GREEN, Colors.YELLOW])

    guess = [Colors.RED, Colors.BLUE, Colors.GREEN, Colors.ORANGE]
    hint = mastermind.get_hint(guess)
    assert mastermind.check_solution(guess) == False

    assert PegColors.RED in hint
    assert hint.count(PegColors.RED) == 3
    assert PegColors.NONE in hint
    assert hint.count(PegColors.NONE) == 1


def test_mastermind_correct_guess(mastermind):

    mastermind.set_solution([Colors.RED, Colors.BLUE, Colors.GREEN, Colors.YELLOW])

    guess = [Colors.RED, Colors.BLUE, Colors.GREEN, Colors.YELLOW]
    hint = mastermind.get_hint(guess)
    assert mastermind.check_solution(guess) == True

    assert PegColors.RED in hint
    assert hint.count(PegColors.RED) == 4
