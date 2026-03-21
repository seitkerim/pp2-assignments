import shutil
import os

# Example 1 - copy
shutil.copy("file1.txt", "copy_file1.txt")

# Example 2 - copy
shutil.copy("file2.txt", "copy_file2.txt")

# Example 3 - delete
if os.path.exists("copy_file2.txt"):
    os.remove("copy_file2.txt")