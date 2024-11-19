number = int(input("Enter : "))
sum_of_digits = 0

while number >= 10:
  sum_of_digits = 0
  for digit in str(number):
    sum_of_digits += int(digit)
  number = sum_of_digits

print("The sum :", number)