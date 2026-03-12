import re
a = input()
b = input()
X = re.findall(rf"{b}",a)
print(len(X))   
