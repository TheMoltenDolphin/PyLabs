inp = input()
n = len(inp)

out = ''
r = 0
for i in range(n - 1):
    if inp[i] == inp[i + 1]:
        r += 1
    else:
        if r > 0:
            out += inp[i]
            out += str(r+1)
            r=0
        else:
            out += inp[i]
out += inp[-1]
print(out)


