string = input("Enter a string: ")
result = ['']
for char in string:
  new_result = []
  for permutation in result:
    for i in range(len(permutation) + 1):
      new_result.append(permutation[:i] + char + permutation[i:])
  result = new_result

print("All permutations of", string, "are:")
for permutation in result:
  print(permutation)