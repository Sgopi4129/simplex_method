def fib(n):
    if n <= 0:
        return []
    sequence = [0, 1]
    while len(sequence) < n:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence[:n]


if __name__ == "__main__":
    try:
        count = int(input("Enter the number of Fibonacci terms: "))
        print(fib(count))
    except ValueError:
        print("Please enter a valid integer.")