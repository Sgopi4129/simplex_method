#write a program to generate and print the fibonacci sequence
import random
def fib(n):
    if n==0:
        return 0
    elif n==1:
        return 1
    else:
        return fib(n-1)+fib(n-2)

def main():
    n=random.randint(1,30)

    for i in range(n):
        print(fib(i),end=" ")

if __name__=="__main__":
    main()