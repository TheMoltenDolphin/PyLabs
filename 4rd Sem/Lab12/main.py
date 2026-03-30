def solve_knapsack(weights, values, capacity):
    n = len(values)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(values[i-1] + dp[i-1][w - weights[i-1]], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]

    max_value = dp[n][capacity]
    
    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected_items.append(i - 1)
            w -= weights[i-1]

    return max_value, selected_items

item_weights = [2, 3, 4, 5]
item_values = [3, 4, 5, 8]
bag_capacity = 5

result_val, result_items = solve_knapsack(item_weights, item_values, bag_capacity)

print(f"Maximum value: {result_val}")
print(f"Selected item indices: {result_items}")