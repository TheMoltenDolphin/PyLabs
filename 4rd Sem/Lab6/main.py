def rabin_karp_search(text, pattern, d=256, q=101):

    n = len(text)
    m = len(pattern)
    h = pow(d, m-1) % q
    p = 0  # хеш паттерна
    t = 0  # хеш текущего окна в тексте
    result = []

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):
        if p == t:
            if text[i:i+m] == pattern:
                result.append(i)

        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            
            if t < 0:
                t = t + q
                
    return result

text = "ABABDABACDABABCABAB"
pattern = "ABABCABAB"
indices = rabin_karp_search(text, pattern)
print(f"Индексы вхождений: {indices}")