#write program to print factorial of a number

def factorial(n):
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


if __name__ == "__main__":
    try:
        number = int(input("Enter a non-negative integer: "))
        print(f"Factorial of {number} is {factorial(number)}")
        
    except ValueError as e:
        print(f"Invalid input: {e}")