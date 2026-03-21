# Example 1
with open("file1.txt", "r") as f:
    print(f.read())

# Example 2
with open("file2.txt", "r") as f:
    for line in f:
        print(line.strip())

# Example 3
with open("file3.txt", "r") as f:
    lines = f.readlines()
    print(lines)