import math
import numpy as np
from scipy.optimize import golden
import matplotlib.pyplot as plt

def f(x):
    return x / (1 + math.sin(x))

x_min = golden(f, brack=(-10, 10))
y_min = f(x_min)

x_max = golden(lambda x: -f(x), brack=(-10, 10))
y_max = f(x_max)

print(f"Минимум: x = {x_min:.4f}, y = {y_min:.4f}")
print(f"Максимум: x = {x_max:.4f}, y = {y_max:.4f}")

x = np.linspace(x_min, x_max, 1000)
y = [f(x_i) for x_i in x]

plt.figure(figsize=(12, 6))
plt.plot(x, y)
plt.scatter([x_min, x_max], [y_min, y_max], color='red', s=100, zorder=5)
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()

period = 2 * math.pi
lower_bound = 3 * math.pi / 2
upper_bound = 7 * math.pi / 2

print("Интервал существования экстремумов:")
print(f"({lower_bound:.4f} + 2πn, {upper_bound:.4f} + 2πn), где n - целое число")
print(f"Это соответствует интервалу длиной {period:.4f}")