inp = "".join(input())
s = list(set(inp))
k = [inp.count(i) for i in s]

def sort_key(i):
    return k["".join(s).find(i)]


sk = sorted(s, key=sort_key)
k = sorted(k)
for i in range(1, 3+1):
    print(sk[-i] + " " + str(k[-i]))