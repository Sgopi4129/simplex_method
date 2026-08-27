# program to find the product of two matrices using random sizes and values

import random


def generate_matrix(rows, cols, value_min=0, value_max=9):
    return [[random.randint(value_min, value_max) for _ in range(cols)] for _ in range(rows)]


def multiply_matrices(a, b):
    rows_a, cols_a = len(a), len(a[0])
    cols_b = len(b[0])
    result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += a[i][k] * b[k][j]
    return result


def print_matrix(matrix):
    for row in matrix:
        print(" ".join(str(value) for value in row))


def main():
    rows_a = random.randint(1, 5)
    cols_a = random.randint(1, 5)
    rows_b = cols_a
    cols_b = random.randint(1, 5)

    matrix_a = generate_matrix(rows_a, cols_a)
    matrix_b = generate_matrix(rows_b, cols_b)

    print(f"Matrix A ({rows_a}x{cols_a}):")
    print_matrix(matrix_a)
    print()

    print(f"Matrix B ({rows_b}x{cols_b}):")
    print_matrix(matrix_b)
    print()

    product = multiply_matrices(matrix_a, matrix_b)
    print(f"Product matrix ({rows_a}x{cols_b}):")
    print_matrix(product)


if __name__ == "__main__":
    main()

