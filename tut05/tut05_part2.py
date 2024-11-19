def is_balanced(string):
  stack = []
  for char in string:
    if char in "({[":
      stack.append(char)
    elif char in")}]":
      if not stack:
        return False
      opening_bracket = stack.pop()
      if not (
        (char == ')' and opening_bracket == '(') or
        (char == '}' and opening_bracket == '{') or
        (char == ']' and opening_bracket == '[')
      ):
        return False
  return not stack

string = input("Enter a string containing parenthesis: ")
if is_balanced(string):
  print("The string is balanced.")
else:
  print("The string is not balanced.")