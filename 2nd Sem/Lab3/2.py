l = [int(i) for i in input("Input list of numbers").split()]
m = [int(i) for i in input("Input list of numbers").split()]

k = set([i for i in l if i in m])

print(len(k))