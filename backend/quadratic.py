#python program to solve quadratic equation
import random

a = float(random.randint(1,100))
b = float(random.randint(1,100))
c = float(random.randint(1,100))

discriminant = b ** 2 - 4 * a * c
print(f"The coefficients are a: {a} b: {b} c: {c}")
if discriminant > 0:
    root1 = (-b + discriminant ** 0.5) / (2 * a)
    root2 = (-b - discriminant ** 0.5) / (2 * a)
    print("Roots are real and different:")
    print("Root 1:", round(root1))
    print("Root 2:", round(root2))
elif discriminant == 0:
    root = -b / (2 * a)
    print("Roots are real and equal:")
    print("Root:", root)
else:
    real_part = -b / (2 * a)
    imag_part = (abs(discriminant) ** 0.5) / (2 * a)
    print("Roots are complex:")
    print(f"Root 1: {round(real_part,5)} + {round(imag_part,5)}j")
    print(f"Root 2: {round(real_part,5)} - {round(imag_part,5)}j")

