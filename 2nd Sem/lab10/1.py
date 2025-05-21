import numpy as np
import matplotlib.pyplot as plt
from scipy.special import legendre

x = np.linspace(-1, 1, 1000)

plots = [(legendre(n)(x), f'- n = {n}') for n in range(1, 8)]

for y_vals, label in plots:
    plt.plot(x, y_vals, label=label)

plt.title("Полиномы Лежандра")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()