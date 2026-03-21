# Example 1
with open("file1.txt", "w") as f:
    f.write("Hello World\n")
    f.write("Python File Handling\n")

# Example 2
with open("file2.txt", "w") as f:
    f.write("This is second file\n")
    f.write("Learning Python\n")

# Example 3
with open("file3.txt", "w") as f:
    for i in range(5):
        f.write(f"Line {i}\n")