s = [i for i in input("введите строки").split()]

d = {}
for i in range(len(s)):
    d[s[i]] = 0
for i in range(len(s)):
    d[s[i]] += 1

for kays, values in d.items():
    print(values, end=" ")
    