import random
from typing import Tuple, List
import pulp

from src.mastermind import Colors, PegColors

class MastermindSolver:

    def __init__(self, mastermind):
        self.mastermind = mastermind

    def create_guess(self) -> list[Colors]:

        return [Colors.RED, Colors.BLUE, Colors.GREEN, Colors.YELLOW]

    def solve(self, quiet=True, write_lp_file=False) -> Tuple[List[Colors], int]:

        guess = self.create_guess()

        guesses = [guess]

        hint = self.mastermind.get_hint(guess)
        iterations = 1

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

        prob += 0, "Objective_Function"

        # create some general constraints:
        # 1. each ball position has exactly one color
        for b in ball_ids:
            constraint_text = f"ball_{b}_has_one_color"
            constraint = pulp.lpSum(x[b][c] for c in color_ids) == 1, constraint_text
            prob += constraint

        # 2. force binary y[c] to be 1 iff any of x[][c] is 1
        for c in color_ids:
            constraint_text = f"color_{c}_exists_lower"
            constraint = y[c] <= pulp.lpSum(x[b][c] for b in ball_ids), ""
            prob += constraint
            constraint_text = f"color_{c}_exists_upper"
            constraint = pulp.lpSum(x[b][c] for b in ball_ids) <= 10000000*y[c], ""
            prob += constraint

        # 3. if duplicates are allowed, we can add a constraint that the number of colors used
        # must be less or equal to the number of colors in the solution.
        # if duplicates are not allowed, the number of colors used must be equal to code length
        constraint_text = "number_of_colors_used"
        if self.mastermind.allow_duplicates:
            constraint = pulp.lpSum(y[c] for c in color_ids) <= self.mastermind.code_length, constraint_text
            prob += constraint
        else:
            constraint = pulp.lpSum(y[c] for c in color_ids) == self.mastermind.code_length, constraint_text
            prob += constraint


        while any(h != PegColors.RED for h in hint):

            if iterations > 10:
                raise Exception(f"Too many iterations. solution: {self.mastermind.solution}")

            # color red represents the number of correct ball colors in the correct position
            constraint_text = f"{iterations}_1"
            constraint = pulp.lpSum(x[b][c] for b,c in enumerate(guess)) == hint.count(PegColors.RED) , constraint_text
            prob += constraint

            # color white represents the number of correct ball colors in the wrong position
            # this cannot be equals because if we have
            # solution: R,B,R,B
            # guess:    R,B,R,R
            # hint:     R,R,R,N
            # then the following constraint would be
            #   y[R] + y[B] + y[R] + y[R] == 3 but since R and B are in the solution then
            # this constraint would lead to infeasibility.
            # Hence we need >=
            constraint_text = f"{iterations}_2"
            constraint = pulp.lpSum(y[c] for c in guess) >= hint.count(PegColors.WHITE) + hint.count(PegColors.RED) , constraint_text
            prob += constraint


            # this constraint is not equals due to the following scenario.
            # solution: R,B,R,B
            # guess:    R,B,B,Y
            # hint:     R,R,W,N
            # if it was equals this constraint would say that
            #   x[0][R] + x[1][R] + x[2][R] + x[3][R]
            # + x[0][B] + x[1][B] + x[2][B] + x[3][B]
            # + x[0][B] + x[1][B] + x[2][B] + x[3][B]
            # + x[0][Y] + x[1][Y] + x[2][Y] + x[3][Y] == 2+1
            # this would force
            # x[0][Y] + x[1][Y] + x[2][Y] + x[3][Y] == 0
            constraint_text = f"{iterations}_3"
            constraint = pulp.lpSum(x[b][c] for c in guess for b in ball_ids) >= hint.count(PegColors.WHITE) + hint.count(PegColors.RED), constraint_text
            prob += constraint

            # The following constraints are not necessary and mathematically equivalent to the above constraints.
            # However, they help the solver to find the solution in less iterations for some reason.
            #constraint = pulp.lpSum(1 - x[b][c] for b,c in enumerate(guess)) == hint.count(PegColors.NONE) + hint.count(PegColors.WHITE), ""
            #prob += constraint

            #constraint_text = f"{iterations}_4"
            #constraint = pulp.lpSum(1 - x[b][c] for b,c in enumerate(guess)) == hint.count(PegColors.WHITE) + hint.count(PegColors.NONE) , constraint_text
            #prob += constraint

            # avoid picking the same color as the previous guess
            prob += pulp.lpSum(y[c] for _,c in enumerate(guess)), "Objective_Function"

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
            guesses.append(guess)
            hint = self.mastermind.get_hint(guess)
            iterations += 1

        if iterations >= 9:
            # write guesses to file
            with open("tmp/guesses.txt", "a") as f:
                f.write(f"Solution: {self.mastermind.solution}\n")
                for i,g in enumerate(guesses, start=1):
                    f.write(f"guess_{i}: {g}\n")
                    f.write(f"hint_{i}: {self.mastermind.get_hint(g)}\n")
                f.write("\n")

        return guess, iterations