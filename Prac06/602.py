def is_even(n):
    return n % 2 == 0

a = int(input())
b = list(map(int,input().split()))
c = filter(is_even, b)
print(len(list(c)))
