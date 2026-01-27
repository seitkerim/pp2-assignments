#1
a = "Hello, World!"
print(len(a)) #length
#2
txt = "The best things in life are free!"
print("free" in txt) 
#3
txt = "The best things in life are free!"
if "free" in txt:
  print("Yes, 'free' is present.")
#4
a = "Hello, World!"
print(a.upper())
a = "Hello, World!"
print(a.lower())
a = " Hello, World! "
print(a.strip()) # returns "Hello, World!"
a = "Hello, World!"
print(a.replace("H", "J")) #Jello, World!
a = "Hello, World!"
print(a.split(",")) # returns ['Hello', ' World!']