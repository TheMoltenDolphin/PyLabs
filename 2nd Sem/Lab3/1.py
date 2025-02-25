l = [int(i) for i in input("Input list of numbers").split()]

l[l.index(max(l))], l[l.index(min(l))] = l[l.index(min(l))], l[l.index(max(l))]

print(l)