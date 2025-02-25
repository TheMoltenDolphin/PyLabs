l = [int(i) for i in input("Input list of numbers").split()]

rl = []
for i in range(1, len(l)):
    if l[i] > l[i - 1]:
        rl.append(l[i])

print(rl)