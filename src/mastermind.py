import random
from typing import List
from enum import Enum

#https://webgamesonline.com/codebreaker/rules.php

class Colors(Enum):
    RED: str = "RED"
    BLUE: str = "BLUE"
    GREEN: str = "GREEN"
    YELLOW: str = "YELLOW"
    ORANGE: str = "ORANGE"
    BROWN: str = "BROWN"
    WHITE: str = "WHITE"
    BLACK: str = "BLACK"

class PegColors(Enum):
    RED: str = "RED" # correct color and position
    WHITE: str = "WHITE" # correct color but wrong position
    NONE: str = "NONE" # color not in solution

class Mastermind:

    code_length: int = 4
    allow_duplicates: bool = True

    def new_game(self) -> List[Colors]:
        colors = list(Colors)
        if self.allow_duplicates:
            self.solution = random.choices(colors, k=self.code_length)
        else:
            self.solution = random.sample(colors, k=self.code_length)

    def check_solution(self, guess: List[Colors]) -> bool:
        return guess == self.solution
    
    def get_hint(self, guess: List[Colors]) -> List[PegColors]:
        hint = []
        for i, color in enumerate(guess):
            if color == self.solution[i]:
                hint.append(PegColors.RED)
            elif color in self.solution:
                hint.append(PegColors.WHITE)
            else:
                hint.append(PegColors.NONE)
        # shuffle the hint
        random.shuffle(hint)
        return hint