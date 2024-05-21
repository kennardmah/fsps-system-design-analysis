def generate_prob_1():
    probabilities = []
    for x1 in range(0, 11):
        for x2 in range(0, 11):
            x1_value = x1
            x2_value = x2
            x3_value = 10 - x1_value - x2_value
            if x1_value + x2_value + x3_value == 10 and x3_value >= 0:
                probabilities.append([round(x1_value*0.1, 1), round(x2_value*0.1, 1), round(x3_value*0.1, 1)])
    return probabilities

import matplotlib.pyplot as plt

probabilities = generate_prob_1()
x = [p[0] for p in probabilities]
y = [p[1] for p in probabilities]
z = [p[2] for p in probabilities]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

plt.show()
