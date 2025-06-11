from src.prof_problem_solver import ProfProblemSolver
from src.utils import showResults


problem = ProfProblemSolver.buildModel()

variables, optimal = ProfProblemSolver.findOptimalSolution(problem)

print(showResults(variables, optimal))