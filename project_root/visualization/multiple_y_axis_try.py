import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.exp(-x)
y3 = 100 * np.cos(x)

fig, ax1 = plt.subplots()

ax1.plot(x, y1, 'b', label='y1 (sin(x)')
ax1.set_xlabel('X-axis')
ax1.set_ylabel('y1', color='b')
ax1.tick_params('y', colors='b')

ax2 = ax1.twinx()

ax2.plot(x, y2, 'g', label='y2 (exp(-x))')
ax2.set_ylabel('y2', color='g')
ax2.tick_params('y', colors='g')

ax3 = ax1.twinx()

ax3.plot(x, y3, 'r', label='y3 (100*cos(x))')
ax3.spines['right'].set_position(('outward', 60))
ax3.set_ylabel('y3', color='r')
ax3.tick_params('y', colors='r')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines3, labels3 = ax3.get_legend_handles_labels()
lines = lines1 + lines2 + lines3
labels = labels1 + labels2 + labels3
plt.legend(lines, labels, loc='upper right')

plt.title('Multiple Y-axis Scales')
plt.show()