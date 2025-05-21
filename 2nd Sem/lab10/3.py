import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

t = np.linspace(0, 2 * np.pi, 1000)

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)

# Настройка графика
ax.set(xlim=(-1.2, 1.2), ylim=(-1.2, 1.2), aspect='equal', title="Анимация фигуры Лисажу")
ax.grid()

def update(frame):
    ratio = frame / 100 or 1e-6  # защита от деления на ноль
    a, b = 1, 1 / ratio
    x, y = np.sin(a * t), np.sin(b * t)
    line.set_data(x, y)
    return line,

ani = FuncAnimation(fig, update, frames=np.arange(0, 101), interval=20, blit=True)

plt.show()
