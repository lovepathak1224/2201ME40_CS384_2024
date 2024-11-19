def normalize_name(name):
    """Convert the student name to lowercase."""
    return name.strip().lower()

def add_student(students_dict, name, grades):
    """Add a new student with grades to the dictionary."""
    students_dict[normalize_name(name)] = grades

def update_grades(students_dict, name, new_grades):
    """Update the grades for an existing student."""
    name = normalize_name(name)
    if name in students_dict:
        students_dict[name] = new_grades
    else:
        print(f"Student '{name}' not found.")

def calculate_average(grades):
    """Calculate the average grade from a list of grades."""
    return sum(grades) / len(grades) if grades else 0

def print_averages(students_dict):
    """Print all students with their average grades."""
    for name, grades in students_dict.items():
        avg_grade = calculate_average(grades)
        print(f"Student: {name.title()}, Average Grade: {avg_grade:.2f}")

def sort_students(students_dict):
    """Sort students by their average grades in descending order."""
    students = [(name, calculate_average(grades)) for name, grades in students_dict.items()]


    for i in range(len(students)):
        for j in range(len(students) - 1):
            if students[j][1] < students[j + 1][1]:
                students[j], students[j + 1] = students[j + 1], students[j]

    return students

def main():
    students_dict = {}

    while True:
        print("\nMenu:")
        print("1. Add a new student")
        print("2. Update grades for an existing student")
        print("3. Print all students with their average grades")
        print("4. Print all students sorted by average grades in descending order")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            name = input("Enter the student's name: ")
            grades = list(map(float, input("Enter the student's grades separated by commas: ").split(',')))
            add_student(students_dict, name, grades)

        elif choice == '2':
            name = input("Enter the student's name: ")
            new_grades = list(map(float, input("Enter the new grades separated by commas: ").split(',')))
            update_grades(students_dict, name, new_grades)

        elif choice == '3':
            print("\nStudents and their average grades:")
            print_averages(students_dict)

        elif choice == '4':
            sorted_students = sort_students(students_dict)
            print("\nStudents sorted by average grades (descending order):")
            for student in sorted_students:
                print(f"Student: {student[0].title()}, Average Grade: {student[1]:.2f}")

        elif choice == '5':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice, please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
