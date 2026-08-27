#program for generating reports for student name with marks using lists

students = []

n = int(input("How many students? "))
for i in range(n):
    name = input(f"Enter name of student {i+1}: ")
    marks = int(input(f"Enter marks for {name}: "))
    students.append([name, marks])

print("\nStudent Report")
print("Name\tMarks")
for student in students:
    print(f"{student[0]}\t{student[1]}")

