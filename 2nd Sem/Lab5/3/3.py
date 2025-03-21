with open("input.txt", encoding='utf-8',  mode="r") as f:
    k = f.readlines()
    s = [i.split() for i in k]
    f.close()

for i in range(len(s)):
    s[i][2] = int(s[i][2])

s.sort(key=lambda x: x[2])

with open("youngest.txt", encoding='utf-8',  mode="w") as f:
    f.write(f"{s[0][0]} {s[0][1]} {s[0][2]}\n")
    f.close()

with open("oldest.txt", encoding='utf-8',  mode="w") as f:
    f.write(f"{s[-1][0]} {s[-1][1]} {s[-1][2]}\n")
    f.close()