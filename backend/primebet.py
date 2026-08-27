#write a program to check whether a number is prime or not

def prime(n):
    if n <= 1:
        return False

    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False

    return True


def main():
    a = int(input("Enter starting position:\t"))
    b = int(input("Enter ending position:\t"))

    if a > b:
        print("Starting position must be less than or equal to ending position.")
        return

    for i in range(a, b + 1):
        if prime(i):
            print(i, end=" ")

    print()


if __name__ == "__main__":
    main()