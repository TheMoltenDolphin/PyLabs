def solve_tsp(matrix):
    n = len(matrix)
    all_visited = (1 << n) - 1
    dp = {}

    def get_path(mask, last_city):
        if mask == all_visited:
            return matrix[last_city][0]

        state = (mask, last_city)
        if state in dp:
            return dp[state]

        best_dist = float('inf')

        for next_city in range(n):
            if not (mask & (1 << next_city)):
                new_dist = matrix[last_city][next_city] + get_path(mask | (1 << next_city), next_city)
                if new_dist < best_dist:
                    best_dist = new_dist

        dp[state] = best_dist
        return best_dist

    return get_path(1, 0)

distance_matrix = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

print(solve_tsp(distance_matrix))