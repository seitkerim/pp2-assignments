import re

s = input()
match = re.search(r"Name: (.+), Age: (.+)", s)

if match:
    print(match.group(1), match.group(2))