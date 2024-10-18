import random
from typing import Tuple, List
import pulp

from src.mastermind import Colors, PegColors

class MastermindSolver:

    def __init__(self, mastermind):
        self.mastermind = mastermind

    def create_guess(self) -> list[Colors]:

        return [Colors.RED, Colors.BLUE, Colors.GREEN, Colors.YELLOW]

        # if self.mastermind.allow_duplicates:
        #     guess = random.choices(colors, k=self.mastermind.code_length)
        # else:
        #     guess = random.sample(colors, k=self.mastermind.code_length)
        # return guess

    def solve(self, quiet=True, write_lp_file=False) -> Tuple[List[Colors], int]:

        iterations = 1

        guess = self.create_guess()

        guesses = [guess]

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

        # 2. force binary y[c] to be 1 iff the color c is used in any ball position
        for c in color_ids:
            constraint = y[c] <= pulp.lpSum(x[b][c] for b in ball_ids), ""
            prob += constraint
            constraint = pulp.lpSum(x[b][c] for b in ball_ids) <= 10000000*y[c], ""
            prob += constraint

        # 3. if duplicates are allowed, we can add a constraint that the number of colors used
        # must be less or equal to the number of colors in the solution.
        # if duplicates are not allowed, the number of colors used must be equal to code length
        if self.mastermind.allow_duplicates:
            constraint = pulp.lpSum(y[c] for c in color_ids) <= self.mastermind.code_length, ""
            prob += constraint

        else:
            constraint = pulp.lpSum(y[c] for c in color_ids) == self.mastermind.code_length, ""
            prob += constraint
        
        # 4. exactly 4 positions and colors are chosen
        # this increases the avg number of iterations to find the solution
        # but decreases the max number of iterations
        # constraint = pulp.lpSum(x[b][c] for b in ball_ids for c in color_ids) == self.mastermind.code_length, ""
        # prob += constraint

        while any(h != PegColors.RED for h in hint):
            iterations += 1

            if iterations > 10:
                raise Exception(f"Too many iterations. solution: {self.mastermind.solution}")

            # color red represents the number of correct ball colors in the correct position
            constraint = pulp.lpSum(x[b][c] for b,c in enumerate(guess)) == hint.count(PegColors.RED) , ""
            prob += constraint

            # color white represents the number of correct ball colors in the wrong position
            constraint = pulp.lpSum(y[c] for c in guess) == hint.count(PegColors.WHITE) + hint.count(PegColors.RED) , ""
            prob += constraint

            # this constraint says that if the hint has a white peg then one of the colors
            # is in the wrong position and hence one of the other ball ids and positions must be larger than the white peg count

            # this constraint is not equals due to the following scenario.
            # assume solutione is R,G,B,Y and guess is R,G,B,R then hint is R,R,R,W
            # if it was equals this constraint would say that
            #             x[1][R] + x[2][R] + x[3][R]
            # + x[0][G]           + x[2][G] + x[3][G]
            # + x[0][B] + x[1][B]           + x[3][B]
            # + x[0][Y] + x[1][Y] + x[2][Y]           == 1
            # forcing x[1][R] + x[2][R] + x[3][R]
            constraint = pulp.lpSum(x[b][c] for i,c in enumerate(guess) for b in ball_ids if i != b) >= hint.count(PegColors.WHITE), f""
            prob += constraint



            # The following constraints are not necessary and mathematically equivalent to the above constraints.
            # However, they help the solver to find the solution in less iterations for some reason.
            constraint = pulp.lpSum(1 - x[b][c] for b,c in enumerate(guess)) == hint.count(PegColors.NONE) + hint.count(PegColors.WHITE), ""
            prob += constraint

            constraint = pulp.lpSum(1 - y[c] for c in guess) == hint.count(PegColors.NONE) , ""
            prob += constraint

            #constraint = pulp.lpSum(1 - x[b][c] for i,c in enumerate(guess) for b in ball_ids if i != b) >= 12 - hint.count(PegColors.NONE) - hint.count(PegColors.WHITE), f"lol2_{iterations}"
            #prob += constraint


            # other heuristics
            # if hint.count(PegColors.RED) == 3 and hint.count(PegColors.WHITE) == 1:
            #     constraint = pulp.lpSum(y[c] for c in color_ids if c not in guess) == 1, ""
            #     prob += constraint


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

        if iterations >= 8:
            # write guesses to file
            with open("tmp/guesses.txt", "w") as f:
                f.write(f"Solution: {self.mastermind.solution}\n")
                for g in guesses:
                    f.write(f"guess: {g}\n")
                    f.write(f"hint: {self.mastermind.get_hint(g)}\n")

        return guess, iterations