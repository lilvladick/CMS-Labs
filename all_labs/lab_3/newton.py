import math
import numpy as np
from scipy.optimize import newton
import matplotlib.pyplot as plt

def f(x):
    return x / (1 + math.sin(x))

# Производная функции
def f_prime(x):
    return (1 + math.sin(x) - x * math.cos(x)) / (1 + math.sin(x))**2

# Вторая производная функции
def f_prime_prime(x):
    return ((2 * math.cos(x) + x * math.sin(x)) * (1 + 2 * math.sin(x) + math.sin(x)**2) - 
            (1 + math.sin(x) - x * math.cos(x)) * (2 * math.cos(x) + 2 * math.sin(x) * math.cos(x))) / (1 + math.sin(x))**4

def find_critical_points(start, end, step=1.0):
    critical_points = []
    x = start
    while x <= end:
        try:
            cp = newton(f_prime, x, tol=1e-6, maxiter=100)

            # проверка на nan и inf
            if not math.isinf(f_prime(cp)) and not math.isnan(f_prime(cp)):
                
                # проверка на уникальность
                if not any(abs(cp - existing_cp) < 1e-4 for existing_cp in critical_points):
                    critical_points.append(cp)
        except (RuntimeError, ZeroDivisionError):
            pass
        x += step
    return critical_points


def classify_critical_point(cp):
    second_f_prime = f_prime_prime(cp)
    if second_f_prime > 0:
        return "Локальный минимум"
    else:
        return "Локальный максимум"

start_range = -10
end_range = 10

critical_points = find_critical_points(start_range, end_range)
critical_points.sort()

for cp in critical_points:
    classification = classify_critical_point(cp)
    print(f"  x = {cp:.4f}: {classification}")

x_values = np.linspace(start_range, end_range, 500)
x_values_filtered = [x for x in x_values if abs(1 + np.sin(x)) > 1e-3]
y_values = [f(x) for x in x_values_filtered]


plt.figure(figsize=(10, 6))
plt.plot(x_values_filtered, y_values, label='f(x)')

for cp in critical_points:
    classification = classify_critical_point(cp)
    if classification == "Локальный минимум":
        plt.plot(cp, f(cp), 'go', label='Локальный минимум' if 'Локальный минимум' not in plt.gca().get_legend_handles_labels()[1] else "") 
    elif classification == "Локальный максимум":
        plt.plot(cp, f(cp), 'ro', label='Локальный максимум' if 'Локальный максимум' not in plt.gca().get_legend_handles_labels()[1] else "") 

plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()

plt.ylim(-10, 25)
plt.xlim(-25, 50)

plt.show()