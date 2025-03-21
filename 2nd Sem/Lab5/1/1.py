i = open("input.txt", "r").readline()
s = [int(i) for i in i.split()]

for i in range(1, len(s)):
    s[i] = s[i] * s[i-1]

open("output.txt", "w").write(str(s[-1]))