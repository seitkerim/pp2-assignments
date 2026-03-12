import re
a = input() 
x = re.findall(r"[A-Z]", a)

print(len(x))