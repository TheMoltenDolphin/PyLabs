def solve_eggs():
    target_floors = 100
    attempts = 0
    dp = [0, 0]
    
    while dp[1] < target_floors:
        attempts += 1
        new_dp_1 = attempts
        new_dp_2 = attempts + dp[1]
        dp = [new_dp_1, new_dp_2]
        
    return attempts

result = solve_eggs()
print(f"Minimum attempts: {result}")