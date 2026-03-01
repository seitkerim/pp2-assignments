# 1. Squares up to N
def squares_up_to_n(n):
    for i in range(n + 1):
        yield i * i


# 2. Even numbers 0 to n (comma separated print example)
def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i


# 3. Numbers divisible by 3 and 4
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 12 == 0:
            yield i


# 4. Squares from a to b
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i


# 5. Countdown from n to 0
def countdown(n):
    for i in range(n, -1, -1):
        yield i