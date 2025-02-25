l = [i for i in input("Input list of strings").split()]
#l=['abc', 'bcd', 'abc', 'abd', 'abd', 'dcd', 'abc']

k=[]

for i in l:
    if i not in k:
        k.append(i)
        print(l.count(i), end=" ")