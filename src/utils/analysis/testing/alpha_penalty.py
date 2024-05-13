"""
getting the E[LCOE] with different alpha_penalty values
"""

import matplotlib.pyplot as plt
import sys
sys.path.append('src/utils/models')
import costModel as cm

sys.path.append('src/utils/analysis')
import expectedPayoff as ep
import cumulativeDistribution as cd

alpha_penalty = [250000 * i for i in range(0, 5)]
graph = []
for alpha in alpha_penalty:
    cm.main(alpha)
    ep.main()
    graph.append([alpha, cd.main()])

results = {}
for alpha_val, values in graph:
    for typ, result in values:
        if typ not in results:
            results[typ] = []
        results[typ].append((alpha_val, result))

# Plotting
fig, ax = plt.subplots()
i = 0
color = [(r/255, g/255, b/255) for r, g, b in [[163, 206, 220], [93, 120, 105], [70, 70, 100],  [118, 118, 118]]]
for typ, points in results.items():
    alpha_vals, res = zip(*points)
    ax.plot(res, alpha_vals, label=typ, color=color[i], marker='o')
    for x, y in zip(res, alpha_vals):
        ax.text(x, y, f'{x:.1f}', ha='center', va='bottom')
    i += 1

ax.set_xlabel('E[LCOE]')
ax.set_ylabel('$ per kW missed')
ax.legend()
plt.show()