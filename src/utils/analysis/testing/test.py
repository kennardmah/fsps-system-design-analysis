import matplotlib.pyplot as plt
import numpy as np

# Example data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Different hatch patterns
patterns = ['/']

for i, pattern in enumerate(patterns):
    # Offset each fill_between for visibility
    plt.fill_between(x, y1 + i*0.5, y2 + i*0.5, hatch=pattern, edgecolor='black', facecolor='none', label=f'Hatch: {pattern}')

plt.legend(loc='upper right')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Different Hatch Patterns in fill_between')
plt.show()