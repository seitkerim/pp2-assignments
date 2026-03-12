import re
a = input()
x = re.search(r"^[a-zA-Z].*[0-9]$", a)
if x:
    print("Yes")
else:
    print("No") 
    