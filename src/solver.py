import random
from typing import Tuple, List
import pulp

from src.mastermind import Colors, PegColors

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

        iterations = 0

        guess = self.create_guess()

        hint = self.mastermind.get_hint(guess)

        if all(c == PegColors.RED for c in hint):
            return guess, iterations

        ball_ids = range(self.mastermind.code_length)
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

        # create some general constraints:
        # 1. each ball position has exactly one color
        for b in ball_ids:
            constraint = pulp.lpSum(x[b][c] for c in color_ids) == 1, ""
            constraints.append(constraint)

        # 2. force binary y[c] to be 1 if the color is used in any ball position
        for c in color_ids:
            constraint = y[c] <= pulp.lpSum(x[b][c] for b in ball_ids), ""
            constraints.append(constraint)
            constraint = pulp.lpSum(x[b][c] for b in ball_ids) <= 100000*y[c], ""
            constraints.append(constraint)

        while any(h != PegColors.RED for h in hint):
            iterations += 1

            if iterations > 100:
                raise Exception("Too many iterations")

            prob = pulp.LpProblem("mastermind_problem", pulp.LpMinimize)
            prob += x[b][Colors.RED], "Objective_Function" # for some reason we need to set this to something. not sure why?


            # color red represents the number of correct ball colors in the correct position
            num_balls_in_correct_position = hint.count(PegColors.RED)
            if num_balls_in_correct_position > 0:
                constraint = pulp.lpSum(x[b][c] for b,c in enumerate(guess)) == num_balls_in_correct_position , ""
                constraints.append(constraint)


            # color none represents the number of ball colors not in the solution at all
            num_balls_not_in_solution = hint.count(PegColors.NONE)
            if num_balls_not_in_solution > 0:
                constraint = pulp.lpSum(1 - y[c] for c in guess) == num_balls_not_in_solution , ""
                constraints.append(constraint)


            # num white represents the number of correct ball colors but in the wrong position
            num_balls_in_wrong_position = hint.count(PegColors.WHITE)
            if num_balls_in_wrong_position > 0:
                constraint = pulp.lpSum(1 - x[b][c] for b,c in enumerate(guess)) == num_balls_in_wrong_position , ""
                constraints.append(constraint)


            # add the constraints
            for c in constraints:
                prob += c


            prob.writeLP(f"tmp/model_{iterations}.lp")

            # solve the problem
            if quiet:
                prob.solve(solver=pulp.PULP_CBC_CMD(timeLimit=60, msg=False))
            else:
                prob.solve()

            status = pulp.LpStatus[prob.status]

            # # reality check
            # for b in ball_ids:
            #     if sum(x[b][c].varValue for c in color_ids) != 1:
            #         lol = [x[b][c].varValue for c in color_ids]
            #         raise Exception(f"Reality check failed for ball {b}. Values: {lol}")

            if status != "Optimal":
                raise Exception(f"No optimal solution found. Status: {status}")

            # get the new guess
            new_guess = self.mastermind.code_length*[None]
            for b in ball_ids:
                for c in color_ids:
                    if x[b][c].varValue == 1:
                        new_guess[b] = c

            guess = new_guess
            hint = self.mastermind.get_hint(guess)
        
        return guess, iterations
