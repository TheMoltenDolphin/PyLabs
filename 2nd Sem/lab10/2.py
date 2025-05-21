import numpy as np
import matplotlib.pyplot as plt

A, B = 1, 1
delta = np.pi / 2
t = np.linspace(0, 2 * np.pi, 1000)

ratios = [(3, 2), (3, 4), (5, 4), (5, 6)]

fig, axs = plt.subplots(2, 2, figsize=(10, 8))

def lissajous(ax, a, b):
    x = A * np.sin(a * t + delta)
    y = B * np.sin(b * t)
    ax.plot(x, y)
    ax.set_title(f"Частоты {a}:{b}")
    ax.set_aspect('equal')
    ax.grid(True)

_ = [lissajous(ax, a, b) for ax, (a, b) in zip(axs.flat, ratios)]

plt.suptitle("Полиномы Лежандра")
plt.tight_layout()
plt.show()
