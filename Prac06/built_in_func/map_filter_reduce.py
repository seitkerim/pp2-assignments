from functools import reduce

numbers = [1,2,3,4,5,6]

# Example 1 map
squares = list(map(lambda x: x*x, numbers))
print(squares)

# Example 2 filter
even = list(filter(lambda x: x%2==0, numbers))
print(even)

# Example 3 reduce
total = reduce(lambda a,b: a+b, numbers)
print(total)