import numpy as np

x = np.array([6, 2, 0, 3, 0, 0, 5, 7, 0]) 

zeros = np.where(x == 0)[0]

after_zeros = zeros + 1
after_zeros = after_zeros[after_zeros < len(x)]

after_zero_values = np.array([x[i] for i in after_zeros ])

print(np.max(after_zero_values))