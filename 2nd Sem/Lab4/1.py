s = [i for i in input("Введите ключ, а после него - данные").split()]
d = {}
for i in range(0, len(s)-1, 2):
    d[s[i]] = s[i+1]
print("Полученное значение -", d[input("Введите ключ")])
