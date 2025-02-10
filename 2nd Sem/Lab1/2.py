n = int(input("Enter a natural number"))
print()
for i in range(n):
    for j in range(1, n-i+1):
        print(j, end="")
    print()


print()


a = "".join([str(i) for i in range(n, 1, -1)])
a = a + "1" + a[::-1]

i = 0
c = 0
print(a)
while i < n:
    b = len(str(n-i))
    c += b
    a = a[b: len(a)-b]
    print(" "*c, end="")
    print(a)
    i+=1