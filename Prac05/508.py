import re
s = input()
d = input() 
x =re.split(rf"{d}",s)
print(*x,sep=",")   