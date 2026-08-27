# write a program to print Pascal's triangle and show the expansion of (a + b)^n
# formula: (a + b)^n = sum_{k=0..n} nCr * a^k * b^(n-k)

import math


def pascal_triangle(rows):
    triangle = []

    for i in range(rows):
        row = [1]

        if triangle:
            last_row = triangle[-1]
            row.extend([last_row[j] + last_row[j + 1] for j in range(len(last_row) - 1)])
            row.append(1)

        triangle.append(row)

    return triangle


# def binomial_expansion(a, b, n):
#     terms = []

#     for k in range(n + 1):
#         coef = math.comb(n, k)
#         power_a = k
#         power_b = n - k

#         parts = []
#         if coef != 1:
#             parts.append(str(coef))
#         if power_a > 0:
#             parts.append(f"{a}^{power_a}" if power_a > 1 else str(a))
#         if power_b > 0:
#             parts.append(f"{b}^{power_b}" if power_b > 1 else str(b))

#         term = "*".join(parts) if parts else "1"
#         terms.append(term)

#     return " + ".join(terms)


def format_pascal_triangle(triangle):
    max_num_width = max(len(str(num)) for row in triangle for num in row)
    last_row = triangle[-1]
    total_width = len(" ".join(str(num).rjust(max_num_width) for num in last_row))

    lines = []
    for row in triangle:
        row_str = " ".join(str(num).rjust(max_num_width) for num in row)
        lines.append(row_str.center(total_width))

    return "\n".join(lines)


def main():
    n = int(input("Enter the exponent n: "))
    if n < 0:
        print("Exponent must be a non-negative integer.")
        return

    a = input("Enter symbol or value for a: ").strip() or "a"
    b = input("Enter symbol or value for b: ").strip() or "b"

    triangle = pascal_triangle(n + 1)

    print("\nPascal's triangle:")
    print(format_pascal_triangle(triangle))

    # expansion = binomial_expansion(a, b, n)
    # print(f"\n({a} + {b})^{n} = {expansion}")


if __name__ == "__main__":
    main()
