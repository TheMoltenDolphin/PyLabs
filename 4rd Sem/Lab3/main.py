def get_next_state(pattern, m, state, x):
    if state < m and x == ord(pattern[state]):
        return state + 1

    for next_s in range(state, 0, -1):
        if ord(pattern[next_s - 1]) == x:
            if pattern[:next_s - 1] == pattern[state - next_s + 1:state]:
                return next_s
    
    return 0

def build_transition_table(pattern, alphabet_size=256):
    m = len(pattern)
    tf = [[0] * alphabet_size for _ in range(m + 1)]

    for state in range(m + 1):
        for x in range(alphabet_size):
            tf[state][x] = get_next_state(pattern, m, state, x)
    return tf

def search(text, pattern):
    m = len(pattern)
    n = len(text)
    tf = build_transition_table(pattern)

    state = 0
    results = []
    for i in range(n):
        state = tf[state][ord(text[i])]
        if state == m:
            results.append(i - m + 1)
            
    return results

text = "ABABDABACDABABCABAB"
pattern = "ABABCABAB"
indices = search(text, pattern)

print(f"Текст: {text}")
print(f"Образец: {pattern}")
print(f"Найден на позициях: {indices}")