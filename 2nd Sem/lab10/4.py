import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def wave(x, A, f):
    return A * np.sin(f * x)

x = np.linspace(0, 10, 1000)
A1_init, f1_init = 1, 1
A2_init, f2_init = 1, 1

fig, axes = plt.subplots(3, 1, figsize=(8, 8))

line1, = axes[0].plot(x, wave(x, A1_init, f1_init), label='Wave 1', color='b')
axes[0].set(title='Wave 1', ylim=(-2, 2), xlabel='x', ylabel='Amplitude')
axes[0].grid(True)

line2, = axes[1].plot(x, wave(x, A2_init, f2_init), label='Wave 2', color='r')
axes[1].set(title='Wave 2', ylim=(-2, 2), xlabel='x', ylabel='Amplitude')
axes[1].grid(True)

line_sum, = axes[2].plot(x, wave(x, A1_init, f1_init) + wave(x, A2_init, f2_init), label='Sum of Waves', color='g')
axes[2].set(title='Sum of Waves', ylim=(-4, 4), xlabel='x', ylabel='Amplitude')
axes[2].grid(True)

axcolor = 'lightgoldenrodyellow'
slider_axes = [
    plt.axes([0.1, 0.01, 0.65, 0.03], facecolor=axcolor),
    plt.axes([0.1, 0.06, 0.65, 0.03], facecolor=axcolor),
    plt.axes([0.1, 0.11, 0.65, 0.03], facecolor=axcolor),
    plt.axes([0.1, 0.16, 0.65, 0.03], facecolor=axcolor)
]

sliders = [
    Slider(slider_axes[0], 'A1', 0.1, 2.0, valinit=A1_init),
    Slider(slider_axes[1], 'f1', 0.1, 10.0, valinit=f1_init),
    Slider(slider_axes[2], 'A2', 0.1, 2.0, valinit=A2_init),
    Slider(slider_axes[3], 'f2', 0.1, 10.0, valinit=f2_init)
]

def update(val):
    A1, f1, A2, f2 = (slider.val for slider in sliders)

    y1 = wave(x, A1, f1)
    y2 = wave(x, A2, f2)
    y_sum = y1 + y2

    line1.set_ydata(y1)
    line2.set_ydata(y2)
    line_sum.set_ydata(y_sum)

    fig.canvas.draw_idle()

for slider in sliders:
    slider.on_changed(update)

plt.subplots_adjust(left=0.1, bottom=0.25)
plt.show()
