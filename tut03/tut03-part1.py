num = int(input("Enter a number: "))
num_str = str(num)
is_rotational_prime = True

for i in range(len(num_str)):
  rotated_num = int(num_str[i:] + num_str[:i])
  is_prime = True
  if rotated_num <= 1:
    is_prime = False
  else:
    for j in range(2, int(rotated_num**0.5) + 1):
      if rotated_num % j == 0:
        is_prime = False
        break
  if not is_prime:
    is_rotational_prime = False
    break

if is_rotational_prime:
  print(num, "is a rotational prime number.")
else:
  print(num, "is not a rotational prime number.")