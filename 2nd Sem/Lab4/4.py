s = [int(i) for i in input()]

d={}
for i in range(10):
    d[i] = 0
    
for i in range(len(s)):
    d[s[i]] += 1

for i in range(10):
    print(d[i], end=" ")

max3 = sorted(list(d.values()))[7:]

for i in range(10):
    if d[i] not in max3:
        del d[i]
    else:
        max3[max3.index(d[i])] = 0

print(d)