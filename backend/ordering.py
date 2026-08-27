#write a python program to sorting of numbers in ascending or descending order
import random

n = random.randint(1,100)
print(f"How many numbers do you want to sort?:{n}")
numbers = []
for i in range(n):
    value = random.randint(1,1000)
    numbers.append(value)

order = input("Enter order (ascending/descending): ").strip().lower()
if order == "descending":
    numbers.sort(reverse=True)
else:
    numbers.sort()

print("Sorted numbers:", " ".join(str(x) for x in numbers))
