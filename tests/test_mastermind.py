from src.solver import Mastermind
from mock import patch

@patch("Mastermind.solution", ["RED", "BLUE", "GREEN", "YELLOW"])
def test_mastermind():
    mastermind = Mastermind()
    mastermind.new_game()
    guess = ["RED", "BLUE", "GREEN", "PINK"]
    assert mastermind.check_solution(guess) == False
    hint = mastermind.get_hint(guess)
    assert hint == ["GREEN", "ORANGE", "GREEN", "None"]
    guess = ["RED", "BLUE", "GREEN", "YELLOW"]
    assert mastermind.check_solution(guess) == True
