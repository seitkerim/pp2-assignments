import re 
a = input()
x = re.search(r"(cat|dog)", a)
if x:
    print("Yes")
else:      
    print("No")