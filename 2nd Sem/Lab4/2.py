s = [i for i in input("Введите ключ, а после него - данные").split()]
d = {}
for i in range(0, len(s)-1, 2):
    d[s[i]] = s[i+1]
inp = input("Введите значение")
v = list(d.values())
for i in range(len(v)):
    if v[i] == inp:
        print("Полученный ключ - ", list(d.keys())[i])