import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

a = 0.2
b = 0.2
c = 5

def system(t, y):
    y1, y2, y3 = y
    dy1_dt = -y2 - y3
    dy2_dt = y1 + a * y2
    dy3_dt = b + y3 * (y1 - c)
    return [dy1_dt, dy2_dt, dy3_dt]

def solution():
    t_span = (0, 100)
    y0 = [1, 1, 1]
    t_eval = np.linspace(*t_span, 1000)

    sol = solve_ivp(system, t_span, y0, t_eval=t_eval)

    # Графики
    t = sol.t
    y1, y2, y3 = sol.y

    plt.figure(figsize=(14, 10))

    plt.subplot(2, 2, 1)
    plt.plot(y1, y2)
    plt.title("Фазовый портрет: y2 от y1")
    plt.xlabel("y1")
    plt.ylabel("y2")

    plt.subplot(2, 2, 2)
    plt.plot(t, y1)
    plt.title("График y1 от t")
    plt.xlabel("t")
    plt.ylabel("y1")

    plt.subplot(2, 2, 3)
    plt.plot(t, y2)
    plt.title("График y2 от t")
    plt.xlabel("t")
    plt.ylabel("y2")

    plt.subplot(2, 2, 4)
    plt.plot(t, y3)
    plt.title("График y3 от t")
    plt.xlabel("t")
    plt.ylabel("y3")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    solution()