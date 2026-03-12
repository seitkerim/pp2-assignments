import re
a = input()
p = input()
if re.search(p,a):
    print("Yes")
else:
    print("No")