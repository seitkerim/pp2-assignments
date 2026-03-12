import re
a = input()

def double_digit(match):
    return match.group() * 2

x = re.sub(r"\d", double_digit, a)
print(x)