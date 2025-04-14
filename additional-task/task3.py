import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def equation_one(t, Y):
    y, dy = Y
    ddy = -2 * dy - 3 * y + np.cos(t)
    return [dy, ddy]

t1 = np.linspace(0, 2 * np.pi, 1000)
sol1 = solve_ivp(equation_one, [0, 2 * np.pi], [0, 0], t_eval=t1)

a = 1
def equation_two(t, Z):
    z, dz = Z
    ddz = a * (1 - z**2) * dz - z
    return [dz, ddz]

t2 = np.linspace(0, 30, 1000)
sol2 = solve_ivp(equation_two, [0, 30], [0, 0], t_eval=t2)

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(sol1.t, sol1.y[0], label="y(t)", color="green")
plt.plot(sol1.t, sol1.y[1], label="y'(t)", color="orange", linestyle="--")
plt.title("Решение: y'' + 2y' + 3y = cos(t)")
plt.xlabel("t")
plt.ylabel("Значения")
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(sol2.t, sol2.y[0], label="z(t)", color="green")
plt.plot(sol2.t, sol2.y[1], label="z'(t)", color="red", linestyle="--")
plt.title("Решение: z'' - a(1-z²)z' + z = 0")
plt.xlabel("t")
plt.ylabel("Значения")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
