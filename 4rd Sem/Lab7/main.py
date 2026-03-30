def find_max_subarray(numbers):
    max_now = max_total = numbers[0]

    for x in numbers[1:]:
        max_now = max(x, max_now + x)
        max_total = max(max_total, max_now)

    return max_total

data = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
result = find_max_subarray(data)
print(result)