inp = input()
n = len(inp)

out = ''
r = 0
i=0
while i != n-1:
    if inp[i+1] in '0123456789':
        out += inp[i]*int(inp[i+1])
        i+=2
    else:
        out += inp[i]
        i+=1

print(out)
