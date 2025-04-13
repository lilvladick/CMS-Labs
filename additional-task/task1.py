import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def ode_func_one(t, y):
    return y**2 - y*t

def ode_func_two(t, y):
    return y**2 + 1

def solution_task_one():
    t_span = (0, 1)
    y0 = [0] # solve_ivp ждет на вход массив начальных условий (0_о)
    t_eval = np.linspace(t_span[0], t_span[1], 100)
    sol_one = solve_ivp(ode_func_one, t_span, y0, t_eval=t_eval)
    sol_two = solve_ivp(ode_func_two, t_span, y0, t_eval=t_eval)

    plt.figure(figsize=(10, 8))

    plt.subplot(2, 1, 1)
    plt.plot(sol_one.t, sol_one.y[0], label='y(t)', color='blue')
    plt.xlabel('Время, t')
    plt.ylabel('y')
    plt.title('Уравнение: dy/dt = y^2 - yt')
    plt.grid(True)
    plt.legend()
    plt.subplot(2, 1, 2)
    plt.plot(sol_two.t, sol_two.y[0], label='y(t)', color='blue')
    plt.xlabel('Время, t')
    plt.ylabel('y')
    plt.title('Уравнение dy/dt = y^2 + 1')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    solution_task_one()