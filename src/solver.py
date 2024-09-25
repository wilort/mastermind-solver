import pulp
from datetime import datetime
from pydantic import BaseModel


class Settings(BaseModel):
    period_start: datetime = datetime(2021,1,1,0,0)
    period_end: datetime = datetime(2021,1,31,0,0)
    use_preassigned_tasks: bool = False
    use_cost_for_unassigned_tasks: bool = False
    use_no_overlapping_tasks: bool = False
    use_max_tasks_in_period: bool = False
    max_tasks_in_period: int = 100
    use_task_requirement: bool = False
    use_fairness: bool = False
    big_number: int = 1000000


class Costs(BaseModel):
    unassigned_task: int = 1


class Model:

    def __init__(
            self,
            tasks: list[Task],
            workers: list[Worker],
            settings: Settings = Settings(),
            costs: Costs = Costs()
            ):

        self.settings = settings
        self.costs = costs
        self.tasks = tasks
        self.workers = workers
        self.worker_ids = [worker.id for worker in self.workers]
        self.task_ids = [task.id for task in self.tasks]

        self.prob = pulp.LpProblem("schedule_problem", pulp.LpMinimize)
        self.objective_function = 0
        self.constraints = []

        # This variable indicates if a worker is assigned a task
        self.x = pulp.LpVariable.dicts(name = "x",
                             indices = (self.worker_ids, self.task_ids),
                             cat = "Binary")

         
        # Add some constraints
        for worker in self.workers:
            if worker.pre_assigned_tasks:
                for task in worker.pre_assigned_tasks:
                    constraint = self.x[worker.id][task.id] == 1, ""
                    self.constraints.append(constraint)

        # Creating the objective function
        self.prob += self.objective_function, "Objective_Function"

        # Adding the constraints
        for constraint in self.constraints:
            self.prob += constraint

    def solve(self, quiet=True):
        if quiet:
            self.prob.solve(pulp.PULP_CBC_CMD(timeLimit=60, msg=False))
        else:
            self.prob.solve()

    def get_results(self):
        unassigned_tasks = []
        for task in self.tasks:
            task_is_not_assigned = sum(self.x[worker.id][task.id].varValue for worker in self.workers) == 0
            if task_is_not_assigned:
                unassigned_tasks.append(task)
        return unassigned_tasks
