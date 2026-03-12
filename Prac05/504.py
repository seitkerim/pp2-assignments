import re
a = input()
x = re.findall(r"\d",a)
if x:
    print(*x,end=" ")
else:
    print("\n")
    