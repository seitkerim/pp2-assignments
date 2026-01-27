#1
x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()

print("Python is " + x)
#2
def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)
#3
x = "awesome"

def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)