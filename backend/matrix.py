import random


class Matrix_multiplication:
    def __init__(self, r1=None, c1=None, r2=None, c2=None, matrix1=None, matrix2=None):
        if r1 is not None and c1 is not None and r2 is not None and c2 is not None:
            self.define_matrix(r1, c1, r2, c2, matrix1, matrix2)

    @staticmethod
    def generate_random_matrix(rows, cols, low=1, high=9):
        return [[random.randint(low, high) for _ in range(cols)] for _ in range(rows)]

    def define_matrix(self, r1, c1, r2, c2, matrix1=None, matrix2=None):
        self.r1 = r1
        self.c1 = c1
        self.r2 = r2
        self.c2 = c2

        if matrix1 is None:
            matrix1 = self.generate_random_matrix(r1, c1)
        if matrix2 is None:
            matrix2 = self.generate_random_matrix(r2, c2)

        if len(matrix1) != r1 or any(len(row) != c1 for row in matrix1):
            raise ValueError("First matrix dimensions do not match the provided shape.")
        if len(matrix2) != r2 or any(len(row) != c2 for row in matrix2):
            raise ValueError("Second matrix dimensions do not match the provided shape.")

        self.matrix1 = matrix1
        self.matrix2 = matrix2
        return self

    def multiplication(self):
        if self.c1 != self.r2:
            raise ValueError("Columns of the first matrix must match rows of the second matrix.")

        result = [[0 for _ in range(self.c2)] for _ in range(self.r1)]

        for i in range(self.r1):
            for j in range(self.c2):
                total = 0
                for k in range(self.c1):
                    total += self.matrix1[i][k] * self.matrix2[k][j]
                result[i][j] = total

        return result


if __name__ == "__main__":
    rows1 = random.randint(1, 10)
    cols1 = random.randint(1, 10)
    rows2 = cols1
    cols2 = random.randint(1, 10)

    matrix = Matrix_multiplication(rows1, cols1, rows2, cols2)
    print("Matrix 1:", matrix.matrix1)
    print("Matrix 2:", matrix.matrix2)
    print("Result:", matrix.multiplication())
