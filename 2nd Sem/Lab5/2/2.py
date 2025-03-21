with open("input.txt", "r") as f:
    s = sorted([int(i) for i in f.readlines()])
    f.close()

with open("output.txt", "w") as f:
    for i in range(len(s)):
        f.write(str(s[i]) + "\n")
    f.close()