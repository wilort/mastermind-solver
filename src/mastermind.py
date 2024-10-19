import random
from typing import List
from enum import Enum
from pydantic import BaseModel

#https://webgamesonline.com/codebreaker/rules.php

class Colors(Enum):
    RED: str = "RED"
    BLUE: str = "BLUE"
    GREEN: str = "GREEN"
    YELLOW: str = "YELLOW"
    WHITE: str = "WHITE"
    BLACK: str = "BLACK"
    #ORANGE: str = "ORANGE"
    #BROWN: str = "BROWN"

class PegColors(Enum):
    RED: str = "RED" # correct color, correct position
    WHITE: str = "WHITE" # correct color, wrong position
    NONE: str = "NONE" # color not in solution

class Mastermind():

    code_length: int = 4
    allow_duplicates: bool = False # THIS MUST BE FALSE RIGHT NOW

    def __init__(self, code_length: int = 4, allow_duplicates: bool = False):
        self.code_length = code_length
        self.allow_duplicates = allow_duplicates

    def new_game(self) -> List[Colors]:
        colors = list(Colors)
        if self.allow_duplicates:
            self.solution = random.choices(colors, k=self.code_length)
        else:
            self.solution = random.sample(colors, k=self.code_length)
    
    def set_solution(self, solution: List[Colors]):
        if self.allow_duplicates:
            self.solution = solution
        else:
            if len(set(solution)) == len(solution):
                self.solution = solution
            else:
                raise ValueError("Solution must not contain duplicates")
            

    def check_solution(self, guess: List[Colors]) -> bool:
        return guess == self.solution
    
    def get_hint_old(self, guess: List[Colors]) -> List[PegColors]:
        hint = []
        for i, color in enumerate(guess):
            if color == self.solution[i]:
                hint.append(PegColors.RED)
            elif color in self.solution:
                hint.append(PegColors.WHITE)
            else:
                hint.append(PegColors.NONE)

        random.shuffle(hint)
        return hint

    def get_hint(self, guess: List[Colors]) -> List[PegColors]:

        hint = []
        index_and_colors_in_correct_position = set()

        for i, color in enumerate(guess):
            if color == self.solution[i]:
                hint.append(PegColors.RED)
                index_and_colors_in_correct_position.add((i, color))

        for i, color in enumerate(guess):
            if (i, color) in index_and_colors_in_correct_position:
                continue
            elif color in self.solution and color not in [c for i, c in index_and_colors_in_correct_position]:
                hint.append(PegColors.WHITE)
            else:
                hint.append(PegColors.NONE)


        random.shuffle(hint)
        return hint