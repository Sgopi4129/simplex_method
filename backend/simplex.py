from itertools import combinations
from numbers import Real


class SimplexMethod:
	"""Solve linear programs with <=, >=, and = constraints."""

	def __init__(self, objective, constraints, limits, relations=None, sense="max", tolerance=1e-9):
		self.objective = list(objective)
		self.constraints = [list(row) for row in constraints]
		self.limits = list(limits)
		self.relations = list(relations or ["<="] * len(self.constraints))
		self.sense = sense.lower()
		self.tolerance = tolerance
		self._validate_input()

	def _validate_input(self):
		variable_count = len(self.objective)

		if variable_count == 0:
			raise ValueError("At least one unknown is required.")
		if not self.constraints:
			raise ValueError("At least one constraint is required.")
		if len(self.constraints) != len(self.limits):
			raise ValueError("Each constraint must have one right-hand-side limit.")
		if len(self.constraints) != len(self.relations):
			raise ValueError("Each constraint must have a relation.")
		if any(len(row) != variable_count for row in self.constraints):
			raise ValueError("Every constraint must contain one coefficient per variable.")
		if any(not isinstance(value, Real) for value in self.objective):
			raise TypeError("Objective coefficients must be numbers.")
		if any(not isinstance(value, Real) for row in self.constraints for value in row):
			raise TypeError("Constraint coefficients must be numbers.")
		if any(not isinstance(value, Real) for value in self.limits):
			raise TypeError("Constraint limits must be numbers.")
		if not isinstance(self.tolerance, Real) or self.tolerance <= 0:
			raise ValueError("Tolerance must be a positive number.")
		if any(relation not in {"<=", ">=", "="} for relation in self.relations):
			raise ValueError("Relations must be <=, >=, or =.")
		if self.sense not in {"max", "min"}:
			raise ValueError("Sense must be max or min.")

	def solve(self):
		variable_count = len(self.objective)
		inequalities = []
		equalities = []
		for coefficients, relation, limit in zip(self.constraints, self.relations, self.limits):
			if relation == "=":
				equalities.append((coefficients, limit))
			elif relation == "<=":
				inequalities.append((coefficients, limit))
			else:
				inequalities.append(([-value for value in coefficients], -limit))
		for variable in range(variable_count):
			boundary = [0.0] * variable_count
			boundary[variable] = -1.0
			inequalities.append((boundary, 0.0))

		candidates = []
		origin = [0.0] * variable_count
		if self._is_feasible(origin, inequalities, equalities):
			candidates.append(origin)
		active_count = variable_count - len(equalities)
		if active_count >= 0:
			for active in combinations(inequalities, active_count):
				point = self._solve_linear_system(
					[row for row, _ in equalities] + [row for row, _ in active],
					[right for _, right in equalities] + [right for _, right in active],
				)
				if point is not None:
					candidates.append(point)

		feasible = [point for point in candidates if self._is_feasible(point, inequalities, equalities)]
		if not feasible:
			raise ValueError("The linear program has no feasible solution.")

		objective_values = [sum(c * x for c, x in zip(self.objective, point)) for point in feasible]
		best_index = (max if self.sense == "max" else min)(range(len(feasible)), key=objective_values.__getitem__)
		solution = feasible[best_index]
		return {"solution": solution, "maximum": objective_values[best_index], "tableau": []}

	def _solve_linear_system(self, matrix, values):
		if len(matrix) != len(values) or len(matrix) != len(self.objective):
			return None
		augmented = [list(row) + [value] for row, value in zip(matrix, values)]
		for column in range(len(self.objective)):
			pivot = max(range(column, len(augmented)), key=lambda row: abs(augmented[row][column]))
			if abs(augmented[pivot][column]) <= self.tolerance:
				return None
			augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
			pivot_value = augmented[column][column]
			augmented[column] = [value / pivot_value for value in augmented[column]]
			for row in range(len(augmented)):
				if row != column:
					factor = augmented[row][column]
					augmented[row] = [value - factor * pivot for value, pivot in zip(augmented[row], augmented[column])]
		return [augmented[row][-1] for row in range(len(augmented))]

	def _is_feasible(self, point, inequalities, equalities):
		return all(sum(a * x for a, x in zip(row, point)) <= limit + self.tolerance for row, limit in inequalities) and all(abs(sum(a * x for a, x in zip(row, point)) - limit) <= self.tolerance for row, limit in equalities) and all(x >= -self.tolerance for x in point)


if __name__ == "__main__":
	problem = SimplexMethod(
		objective=[3, 5, 2],
		constraints=[[1, 0, 1], [0, 2, 1], [3, 2, 0], [1, 1, 1]],
		limits=[4, 12, 18, 10],
		relations=["<=", ">=", "=", "<="],
	)
	result = problem.solve()
	print("Variables:", result["solution"])
	print("Maximum:", result["maximum"])

