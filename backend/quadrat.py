#write a program for finding roots of quadratic equation
import math
import random

global root1,root2
def quadr(a,b,c):
    print("You given numbers are:",a,b,c)
    disc=b*b-4*a*c
    if disc>0:
        root1=((-b+math.sqrt(disc))/(2*a))
        root2=((-b-math.sqrt(disc))/(2*a))
        return root1,root2

    elif disc==0:
        root1=root2=(-b/(2*a))
        return root1,root2
    
    elif disc<0:
        root1=(-b/(2*a))
        root2=((abs(disc)**0.5)/(2*a))
        return f"{root1}+i {root2} and {root1}-i {root2}"

def main():
    print(f"The roots are:{quadr(random.randint(1,10),random.randint(1,10),random.randint(1,10))}")

if __name__=="__main__":
    main()

        