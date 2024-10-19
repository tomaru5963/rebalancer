from collections import deque

from .portfolio import Portfolio
from .problem import Problem, Status


class Solver:
    def __init__(self, portfolio: Portfolio):
        self.stack: deque[Problem] = deque()
        problem = Problem.from_portfolio(portfolio)
        self.stack.append(problem)

        """
        tentative_solution = problem.model_copy(deep=True)
        for asset in tentative_solution.portfolio:
            for instrument in asset.instruments:
                instrument.units = 0
        tentative_solution.fit()
        self.tentative_solution = tentative_solution
        """
        self.tentative_solution: Problem | None = None

    def solve(self) -> Problem | None:
        while len(self.stack) > 0:
            problem = self.stack.pop()
            status = problem.fit()
            if status is Status.unfeasible:
                continue
            if status is Status.candidate:
                if self.tentative_solution is None:
                    self.tentative_solution = problem
                    continue
                if (problem.objective_value <
                        self.tentative_solution.objective_value):
                    self.tentative_solution = problem
                continue
            assert status is Status.optimal

            if self.tentative_solution is not None:
                if (problem.objective_value >=
                        self.tentative_solution.objective_value):
                    continue
            left, right = problem.branch()
            self.stack.append(left)
            self.stack.append(right)

        return self.tentative_solution
