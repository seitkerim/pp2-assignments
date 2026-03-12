import re
a = input()
nums = re.findall(r"\d{2,}", a)
print(*nums, end=" ")