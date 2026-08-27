import json
from http.server import BaseHTTPRequestHandler
from itertools import combinations
from numbers import Real


class SimplexMethod:
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
        if variable_count == 0 or not self.constraints:
            raise ValueError("At least one unknown and one constraint are required.")
        if len(self.constraints) != len(self.limits) or len(self.constraints) != len(self.relations):
            raise ValueError("Each constraint must have one relation and one limit.")
        if any(len(row) != variable_count for row in self.constraints):
            raise ValueError("Every constraint must contain one coefficient per variable.")
        if any(not isinstance(value, Real) for value in self.objective + self.limits):
            raise TypeError("Objective coefficients and limits must be numbers.")
        if any(not isinstance(value, Real) for row in self.constraints for value in row):
            raise TypeError("Constraint coefficients must be numbers.")
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
        for active in combinations(inequalities, variable_count - len(equalities)):
            point = self._solve_linear_system(
                [row for row, _ in equalities] + [row for row, _ in active],
                [right for _, right in equalities] + [right for _, right in active],
            )
            if point is not None and self._is_feasible(point, inequalities, equalities):
                candidates.append(point)
        if not candidates:
            raise ValueError("The linear program has no feasible solution.")

        values = [sum(coefficient * value for coefficient, value in zip(self.objective, point)) for point in candidates]
        best = (max if self.sense == "max" else min)(range(len(candidates)), key=values.__getitem__)
        return {"solution": candidates[best], "maximum": values[best]}

    def _solve_linear_system(self, matrix, values):
        size = len(self.objective)
        if len(matrix) != size:
            return None
        augmented = [list(row) + [value] for row, value in zip(matrix, values)]
        for column in range(size):
            pivot = max(range(column, size), key=lambda row: abs(augmented[row][column]))
            if abs(augmented[pivot][column]) <= self.tolerance:
                return None
            augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
            pivot_value = augmented[column][column]
            augmented[column] = [value / pivot_value for value in augmented[column]]
            for row in range(size):
                if row != column:
                    factor = augmented[row][column]
                    augmented[row] = [value - factor * pivot for value, pivot in zip(augmented[row], augmented[column])]
        return [augmented[row][-1] for row in range(size)]

    def _is_feasible(self, point, inequalities, equalities):
        return all(sum(a * x for a, x in zip(row, point)) <= limit + self.tolerance for row, limit in inequalities) and all(abs(sum(a * x for a, x in zip(row, point)) - limit) <= self.tolerance for row, limit in equalities) and all(x >= -self.tolerance for x in point)


class handler(BaseHTTPRequestHandler):
    def _send_json(self, payload, status=200):
        response = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def do_OPTIONS(self):
        self._send_json({})

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length))
            result = SimplexMethod(data["objective"], data["constraints"], data["limits"], data.get("relations"), data.get("sense", "max")).solve()
            self._send_json(result)
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
            self._send_json({"error": str(error)}, 400)
