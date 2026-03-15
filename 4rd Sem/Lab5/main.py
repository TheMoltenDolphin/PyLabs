def bad_character_table(pattern):
    bad_char = {}
    for i in range(len(pattern)):
        bad_char[pattern[i]] = i
    return bad_char

def boyer_moore_search(text, pattern):
    n = len(text)
    m = len(pattern)
    
    if m == 0: return 0
    
    bad_char = bad_character_table(pattern)
    
    s = 0  
    occurrences = []
    
    while s <= (n - m):
        j = m - 1
        
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
            
        if j < 0:
            occurrences.append(s)
            s += (m - bad_char.get(text[s + m], -1) if s + m < n else 1)
        else:
            char_in_text = text[s + j]
            s += max(1, j - bad_char.get(char_in_text, -1))
            
    return occurrences

# Тест
text = "ABABDABACDABABCABAB"
pattern = "ABABCABAB"
print(f"Индексы вхождений: {boyer_moore_search(text, pattern)}")