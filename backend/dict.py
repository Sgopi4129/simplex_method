#write a python program to create a dictionary

d = {}
n = int(input("How many items in the dictionary? "))
for i in range(n):
    key = input(f"Enter key {i+1}: ")
    value = input(f"Enter value for {key}: ")
    d[key] = value

print("\nCreated dictionary:")
for key, value in d.items():
    print(f"{key}: {value}")
