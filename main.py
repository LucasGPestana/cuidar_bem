from src.prof_problem_solver import ProfProblemSolver
from src.utils import showResults


problem = ProfProblemSolver.buildModel()

variables, optimal, sv_values = ProfProblemSolver.findOptimalSolution(problem)

print(showResults(variables, optimal, sv_values))