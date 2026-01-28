import itertools

def solve():
    
    k = 4
    
    raw_permutations = itertools.permutations("КОМБИНАТОРИКА", k)

    unique_words = set("".join(p) for p in raw_permutations)
    
    count = len(unique_words)

    print(len(unique_words))
    

if __name__ == "__main__":
    solve()