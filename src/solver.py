import random
from typing import List
from pydantic import BaseModel

#https://webgamesonline.com/codebreaker/rules.php

class Colors(BaseModel):
    RED: str = "RED"
    BLUE: str = "BLUE"
    GREEN: str = "GREEN"
    YELLOW: str = "YELLOW"
    ORANGE: str = "ORANGE"
    BROWN: str = "BROWN"
    WHITE: str = "WHITE"
    BLACK: str = "BLACK"

class PegColors(BaseModel):
    RED: str = "RED" # correct color and position
    WHITE: str = "WHITE" # correct color but wrong position
    NONE: str = "NONE" # color not in solution

class Mastermind:

    code_length: int = 4
    allow_duplicates: bool = True

    def new_game(self) -> List[Colors]:
        self.solution = [random.choice(Colors.model_fields.keys()) for _ in range(self.code_length)]

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

# class Model:

#     def __init__(
#             self,
#             tasks: list[Task],
#             workers: list[Worker],
#             settings: Settings = Settings(),
#             costs: Costs = Costs()
#             ):

#         self.settings = settings
#         self.costs = costs
#         self.tasks = tasks
#         self.workers = workers
#         self.worker_ids = [worker.id for worker in self.workers]
#         self.task_ids = [task.id for task in self.tasks]

#         self.prob = pulp.LpProblem("schedule_problem", pulp.LpMinimize)
#         self.objective_function = 0
#         self.constraints = []

#         # This variable indicates if a worker is assigned a task
#         self.x = pulp.LpVariable.dicts(name = "x",
#                              indices = (self.worker_ids, self.task_ids),
#                              cat = "Binary")

         
#         # Add some constraints
#         for worker in self.workers:
#             if worker.pre_assigned_tasks:
#                 for task in worker.pre_assigned_tasks:
#                     constraint = self.x[worker.id][task.id] == 1, ""
#                     self.constraints.append(constraint)

#         # Creating the objective function
#         self.prob += self.objective_function, "Objective_Function"

#         # Adding the constraints
#         for constraint in self.constraints:
#             self.prob += constraint

#     def solve(self, quiet=True):
#         if quiet:
#             self.prob.solve(pulp.PULP_CBC_CMD(timeLimit=60, msg=False))
#         else:
#             self.prob.solve()

#     def get_results(self):
#         unassigned_tasks = []
#         for task in self.tasks:
#             task_is_not_assigned = sum(self.x[worker.id][task.id].varValue for worker in self.workers) == 0
#             if task_is_not_assigned:
#                 unassigned_tasks.append(task)
#         return unassigned_tasks
