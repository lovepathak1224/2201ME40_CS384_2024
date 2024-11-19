s = input("Enter : ")
compressed_string = ""
count = 0
current_char = None

for char in s:
  if char == current_char:
    count += 1
  else:
    if current_char:
      compressed_string += current_char + str(count)
    current_char = char
    count = 1

if current_char:
  compressed_string += current_char + str(count)

print(f"Compressed string: {compressed_string}")