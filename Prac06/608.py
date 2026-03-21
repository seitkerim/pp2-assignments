a = int(input())
b = list(map(int,input().split()))
res = sorted(set(b))
print(*res)
