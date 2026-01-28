import numpy as np

def solve():
    N = 15
    M = 15
    
    dp = np.zeros((N + 1, M + 1), dtype=object)
    

    for i in range(N + 1): dp[i][0] = 1
    for j in range(M + 1): dp[0][j] = 1
        
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
            
    ans1 = dp[N][M]
    

    
    dp2 = np.zeros((N + 1, M + 1, 2), dtype=object)
    
    for i in range(1, N + 1):
        dp2[i][0][0] = 1 
        dp2[i][0][1] = 0
        
    dp2[0][1][1] = 1
    
    for x in range(1, N + 1):
        for y in range(1, M + 1):
            dp2[x][y][0] = dp2[x-1][y][0] + dp2[x-1][y][1]
            dp2[x][y][1] = dp2[x][y-1][0]
            
    ans2 = dp2[N][M][0] + dp2[N][M][1]
    
    print(ans1 ,ans2)


if __name__ == "__main__":
    solve()