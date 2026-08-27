import random

def transpose(a,m,n):
    print("The original matrix")
    for i in range(m):
        for j in range(n):
            print(a[i][j],end=" ")
        print()

    for i in range(m):
        for j in range(i, n):
            a[i][j], a[j][i] = a[j][i], a[i][j]


    print("After the transpose matrix")

    for i in range(m):
        for j in range(n):
            print(a[i][j],end=" ")
        print()

def main():
    m = n = random.randint(1, 10)
    print(f"The dimensions of matrix are {m} rows  and {n} columns")
    a = [[random.randint(1, 100) for j in range(n)] for i in range(m)]
    transpose(a, m, n)


if __name__=="__main__":
    main()