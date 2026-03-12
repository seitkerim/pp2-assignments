import re

text = "HelloWorld Python_is_good abbb abb ab acb a123b camelCaseString snake_case_string"

# 1. 'a' followed by zero or more 'b'
pattern1 = r"ab*"
print("1:", re.findall(pattern1, text))


# 2. 'a' followed by 2-3 'b'
pattern2 = r"ab{2,3}"
print("2:", re.findall(pattern2, text))


# 3. lowercase letters joined with underscore
pattern3 = r"[a-z]+_[a-z]+"
print("3:", re.findall(pattern3, text))


# 4. one uppercase followed by lowercase
pattern4 = r"[A-Z][a-z]+"
print("4:", re.findall(pattern4, text))


# 5. 'a' followed by anything ending in 'b'
pattern5 = r"a.*?b"
print("5:", re.findall(pattern5, text))


# 6. replace space, comma, dot with colon
text6 = "Hello, world. Python is good"
result6 = re.sub(r"[ ,\.]", ":", text6)
print("6:", result6)


# 7. snake_case to camelCase
snake = "snake_case_string"
camel = re.sub(r"_([a-z])", lambda x: x.group(1).upper(), snake)
print("7:", camel)


# 8. split string at uppercase letters
camel_text = "HelloWorldPython"
result8 = re.split(r"(?=[A-Z])", camel_text)
print("8:", result8)


# 9. insert spaces before capital letters
result9 = re.sub(r"([A-Z])", r" \1", camel_text).strip()
print("9:", result9)


# 10. camelCase to snake_case
camel2 = "camelCaseString"
snake2 = re.sub(r"([A-Z])", r"_\1", camel2).lower()
print("10:", snake2)