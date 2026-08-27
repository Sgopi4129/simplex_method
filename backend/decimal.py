# Program to convert Binary to Decimal

def decimal(num):
    dec = 0
    i = 0

    while num > 0:
        rem = num % 10      # Extract last binary digit
        dec = dec + rem * (2 ** i)
        num = num // 10     # Remove last digit
        i += 1

    return dec


def main():
    num = int(input("Enter a binary number: "))
    print("Decimal number =", decimal(num))


if __name__ == "__main__":
    main()