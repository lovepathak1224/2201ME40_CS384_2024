import re

def validate_password(password, criteria):
    if len(password) < 8:
        print(f"'{password}' is Invalid. Less than 8 Characters.")
        return False

    uppercase = re.compile(r'[A-Z]')
    lowercase = re.compile(r'[a-z]')
    numbers = re.compile(r'[0-9]')
    special_characters = re.compile(r'[!@#]')

    criteria_checks = {
        '1': uppercase.search(password),
        '2': lowercase.search(password),
        '3': numbers.search(password),
        '4': special_characters.search(password)
    }

    if re.search(r'[^a-zA-Z0-9!@#]', password):
        print(f"'{password}' is Invalid. It contains forbidden characters.")
        return False

    for i in criteria:
        if not criteria_checks[i]:
            print(f"'{password}' is Invalid. Missing criteria {i}.")
            return False

    print(f"'{password}' is Valid.")
    return True

# password_list
password_list = [
    "abc12345",
    "abc",
    "123456789",
    "abcdefg$",
    "abcdefgABHD!@313",
    "abcdefgABHD$$!@313"
]

print("Select criteria for password validation:")
print("1: Uppercase letters (A-Z)")
print("2: Lowercase letters (a-z)")
print("3: Numbers (0-9)")
print("4: Special characters (!, @, #)")

criteria = input("Enter the criteria that you want to check: ").split(',')

for password in password_list:
    validate_password(password,criteria)


def read_passwords_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]


file_path = "input.txt"
password_list = read_passwords_from_file(file_path)

print("Select criteria for password validation:")
print("1: Uppercase letters (A-Z)")
print("2: Lowercase letters (a-z)")
print("3: Numbers (0-9)")
print("4: Special characters (!, @, #)")

criteria = input("Enter the criteria that you want to check : ").split(',')

valid_count = 0
invalid_count = 0

for password in password_list:
    if validate_password(password, criteria):
        valid_count += 1
    else:
        invalid_count += 1

print(f"Total valid passwords: {valid_count}")
print(f"Total invalid passwords: {invalid_count}")