import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

g1 = 0.0005      # коэффициент внутривидовой конкуренции жертвы
r1 = 0.5         # прирост популяции жертв
lambda1 = 0.01   # взаимодействие хищник-жертва (уничтожение жертв)
lambda2 = 0.01   # взаимодействие хищник-жертва (рост хищников)
beta2 = 0.2      # естественная смертность хищников
x0 = 25          # начальная популяция жертв
y0 = 5           # начальная популяция хищников

t_span = (0, 1000)
t_eval = np.linspace(*t_span, 1000)
initial_conditions = [x0, y0]

def predator_prey_classic(t, state):
    x, y = state
    dx_dt = r1 * x - lambda1 * x * y
    dy_dt = lambda2 * x * y - beta2 * y
    return [dx_dt, dy_dt]

sol_classic = solve_ivp(predator_prey_classic, t_span, initial_conditions, t_eval=t_eval)
x_classic, y_classic = sol_classic.y

def predator_prey_competition(t, state):
    x, y = state
    dx_dt = r1 * x - lambda1 * x * y - g1 * x**2
    dy_dt = lambda2 * x * y - beta2 * y
    return [dx_dt, dy_dt]

sol_comp = solve_ivp(predator_prey_competition, t_span, initial_conditions, t_eval=t_eval)
x_comp, y_comp = sol_comp.y

plt.figure(figsize=(14, 10))

plt.subplot(2, 2, 1)
plt.plot(sol_classic.t, x_classic, label='Жертвы (x)', color='blue')
plt.plot(sol_classic.t, y_classic, label='Хищники (y)', color='red')
plt.xlabel('Время, t')
plt.ylabel('Плотность')
plt.title('Плотность популяций от времени (классическая модель)')
plt.legend()
plt.grid(True)

plt.subplot(2, 2, 2)
plt.plot(x_classic, y_classic, color='blue')
plt.xlabel('Жертвы (x)')
plt.ylabel('Хищники (y)')
plt.title('Фазовый портрет (классическая модель)')
plt.grid(True)

plt.subplot(2, 2, 3)
plt.plot(sol_comp.t, x_comp, label='Жертвы (x)', color='blue')
plt.plot(sol_comp.t, y_comp, label='Хищники (y)', color='red')
plt.xlabel('Время, t')
plt.ylabel('Плотность')
plt.title('Плотность популяций от времени (с внутривидовой конкуренцией)')
plt.legend()
plt.grid(True)

plt.subplot(2, 2, 4)
plt.plot(x_comp, y_comp, color='blue')
plt.xlabel('Жертвы (x)')
plt.ylabel('Хищники (y)')
plt.title('Фазовый портрет (с внутривидовой конкуренцией)')
plt.grid(True)

plt.tight_layout()
plt.show()
