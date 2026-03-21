a = int(input())
b= map(int,input().split())
c = map(int, input().split())
s = 0
for b,c in zip(b,c):
    s += b * c

print(s)