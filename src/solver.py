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

    def solve(self, quiet=True, write_lp_file=False) -> Tuple[List[Colors], int]:

        iterations = 0

        guess = self.create_guess()

        hint = self.mastermind.get_hint(guess)

        if all(c == PegColors.RED for c in hint):
            return guess, iterations

        ball_ids = range(self.mastermind.code_length)
        color_ids = list(Colors)

        prob = pulp.LpProblem("mastermind_problem", pulp.LpMinimize)

        # the variable x[b][c] is 1 iff ball b has color c
        x = pulp.LpVariable.dicts(name = "x",
                              indices = (ball_ids, color_ids),
                              cat = "Binary")
        
        # the variable y[c] is 1 iff color c exists in the solution
        y = pulp.LpVariable.dicts(name = "y",
                                indices = color_ids,
                                cat = "Binary")

        # for some reason we need to set this to something. not sure why?
        prob += x[0][Colors.RED], "Objective_Function" 

        # create some general constraints:
        # 1. each ball position has exactly one color
        for b in ball_ids:
            constraint = pulp.lpSum(x[b][c] for c in color_ids) == 1, ""
            prob += constraint

        # 2. force binary y[c] to be 1 iff the color is used in any ball position
        for c in color_ids:
            constraint = y[c] <= pulp.lpSum(x[b][c] for b in ball_ids), ""
            prob += constraint
            constraint = pulp.lpSum(x[b][c] for b in ball_ids) <= 100000*y[c], ""
            prob += constraint

        # 3. if duplicates are allowed, we can add a constraint that the number of colors used
        # must be less or equal to the number of colors in the solution.
        # if duplicates are not allowed, the number of colors used must be equal to the number of colors in the solution.
        if self.mastermind.allow_duplicates:
            constraint = pulp.lpSum(y[c] for c in color_ids) <= self.mastermind.code_length, ""
            prob += constraint
        else:
            constraint = pulp.lpSum(y[c] for c in color_ids) == self.mastermind.code_length, ""
            prob += constraint

            # a color can only be chosen once
            #for c in color_ids:
            #    constraint = pulp.lpSum(x[b][c] for b in ball_ids) <= 1, ""
            #    prob += constraint

        while any(h != PegColors.RED for h in hint):
            iterations += 1

            if iterations > 11:
                raise Exception(f"Too many iterations. solution: {self.mastermind.solution}")


            # color red represents the number of correct ball colors in the correct position
            if hint.count(PegColors.RED) > 0:
                constraint = pulp.lpSum(x[b][c] for b,c in enumerate(guess)) == hint.count(PegColors.RED) , ""
                prob += constraint


            # color non represents the number of colors that are not in the solution
            # to make this ready for duplicates, us c in set(guess) and rhs = min(unique colors in guess, num none in hint)
            if hint.count(PegColors.NONE) > 0:
                constraint = pulp.lpSum(1 - y[c] for c in guess) == hint.count(PegColors.NONE), ""
                prob += constraint


            # color white represents the number of correct ball colors but in the wrong position
            # I suspect this constraint is not giving as much information
            # as it could do.
            if hint.count(PegColors.WHITE) > 0:
                constraint = pulp.lpSum(1 - x[b][c] for b,c in enumerate(guess)) >= hint.count(PegColors.WHITE) , ""
                prob += constraint

            if write_lp_file:
                prob.writeLP(f"tmp/model_{iterations}.lp")

            # solve the problem
            if quiet:
                prob.solve(solver=pulp.PULP_CBC_CMD(timeLimit=60, msg=False))
            else:
                prob.solve()

            status = pulp.LpStatus[prob.status]

            if status != "Optimal":
                raise Exception(f"No optimal solution found. Status: {status}, iterations: {iterations}, guess: {guess}, hint: {hint}")

            new_guess = self.mastermind.code_length*[None]
            for b in ball_ids:
                for c in color_ids:
                    if x[b][c].varValue == 1:
                        new_guess[b] = c

            guess = new_guess
            hint = self.mastermind.get_hint(guess)
        
        return guess, iterations
