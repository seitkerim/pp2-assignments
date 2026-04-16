text = "here and there, know-hows and how-tos, 1960s and 1975"

import re
x = re.findall(r"\w+[-]\w+" , text)
print(x)
print(x)