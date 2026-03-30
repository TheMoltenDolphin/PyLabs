def count_ways(amount, coins):
    dp = [0] * (amount + 1)
    dp[0] = 1
    
    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] += dp[x - coin]
            
    return dp[amount]

sum_to_make = 5
coin_types = [1, 2, 5]

result = count_ways(sum_to_make, coin_types)
print(result)