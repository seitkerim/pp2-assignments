import re
a = input()
x = re.compile("^\d+$")
if x.fullmatch(a):
    print("Match")
else:
    print("No match")
