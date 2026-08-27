def fact(num):
    if num < 0:
        raise ValueError("Negative number is not allowed")
    if num == 0:
        return 1
    return num * fact(num - 1)


def main():
    n = int(input("Enter n value:\t"))
    r = int(input("Enter r value:\t"))

    try:
        if n < 0 or r < 0:
            raise ValueError("Negative number is not allowed")
        if n < r:
            raise ValueError("n must be greater than or equal to r")

        bino = fact(n) // (fact(r) * fact(n - r))
        print(bino)

    except ValueError as e:
        print(e)

if __name__=="__main__":
    main()
