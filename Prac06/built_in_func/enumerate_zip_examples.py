names = ["Ali", "Sara", "John"]
scores = [90,85,88]

# Example 1 enumerate
for index, name in enumerate(names):
    print(index, name)

# Example 2 zip
for name, score in zip(names, scores):
    print(name, score)

# Example 3 type conversion
num = "10"
print(int(num) + 5)
print(type(num))