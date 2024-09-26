import random
from typing import Tuple, List
import pulp

from src.mastermind import Colors

class MastermindSolver:

    def __init__(self, mastermind):
        self.mastermind = mastermind
    
    def create_guess(self) -> list[Colors]:
        colors = list(Colors)
        if self.mastermind.allow_duplicates:
            guess = random.choices(colors, k=self.mastermind.code_length)
        else:
            guess = random.sample(colors, k=self.mastermind.code_length)
        return guess

    def solve(self, quiet=True) -> Tuple[List[Colors], int]:

        # create random guess
        guess = self.create_guess()
        iterations = 0

        # get hint
        hint = self.mastermind.get_hint(guess)

        if hint == [Colors.RED]*self.mastermind.code_length:
            return guess

        ball_ids = range(1, self.mastermind.code_length + 1)
        color_ids = list(Colors)

        # the variable x[b][c] is 1 iff ball b has color c
        x = pulp.LpVariable.dicts(name = "x",
                              indices = (ball_ids, color_ids),
                              cat = "Binary")
        
        # the variable y[c] is 1 iff color c exists in the solution
        y = pulp.LpVariable.dicts(name = "y",
                                indices = color_ids,
                                cat = "Binary")
        constraints = []

        # create the general constraint:
        # Total numbers of balls should be equal to the code length
        num_chosen_balls = pulp.lpSum(x[b][c] for b in ball_ids for c in color_ids)
        constraint = num_chosen_balls == self.mastermind.code_length, ""
        constraints.append(constraint)

        for c in color_ids:
            constraint = y[c] <= pulp.lpSum(x[b][c] for b in ball_ids), ""
            constraints.append(constraint)
            constraint = pulp.lpSum(x[b][c] for b in ball_ids) <= 4*y[c], ""
            constraints.append(constraint)


        while hint != [Colors.RED]*self.mastermind.code_length:
            iterations += 1

            prob = pulp.LpProblem("mastermind_problem", pulp.LpMinimize)
            self.prob += 0, "Objective_Function"

            # color red represents the number of correct ball colors in the correct position
            num_balls_in_correct_position = hint.count(Colors.RED)
            if num_balls_in_correct_position > 0:
                constraint = pulp.lpSum(x[b][c] for b,c in enumerate(guess)) == num_balls_in_correct_position , ""
                constraints.append(constraint)


            # color none represents the number of ball colors not in the solution at all
            num_balls_not_in_solution = hint.count(Colors.NONE)
            if num_balls_not_in_solution > 0:
                constraint = pulp.lpSum(1 - y[c] for c in guess) == num_balls_not_in_solution , ""
                constraints.append(constraint)

            # num white represents the number of correct ball colors but in the wrong position
            num_balls_in_wrong_position = hint.count(Colors.WHITE)
            if num_balls_in_wrong_position > 0:

                # if x balls are in the wrong position we know that the inverse sum of the balls will b x
                constraint = pulp.lpSum(1 - x[b][c] for b,c in enumerate(guess)) == num_balls_in_wrong_position , ""
                constraints.append(constraint)

            # add the constraints
            prob += constraints

            # solve the problem
            if quiet:
                prob.solve(pulp.PULP_CBC_CMD(timeLimit=60, msg=False))
            else:
                prob.solve()

            # get the new guess
            
            new_guess = []
            for b in ball_ids:
                for c in color_ids:
                    if x[b][c].varValue == 1:
                        new_guess.append(c)

            guess = new_guess
            hint = self.mastermind.get_hint(guess)
        
        return guess, iterations
