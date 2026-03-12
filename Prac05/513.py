import re
a = input()
x = re.findall(r"\w+", a)
print(len(x))