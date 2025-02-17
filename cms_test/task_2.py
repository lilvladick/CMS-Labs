import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Чтение данных из CSV-файла
data = pd.read_csv('data.csv')
x = data['vodichka']
y = data['volosi']

def add_text(ax, text):
    ax.text(0.05, 0.95, text, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))

fig, axs = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('Модели зависимости содержания свинца в волосах от его содержания в питьевой воде')

# Линейная модель
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
line = slope * x + intercept
axs[0, 0].scatter(x, y)
axs[0, 0].plot(x, line, color='r')
axs[0, 0].set_title('Линейная модель')
add_text(axs[0, 0], f'y = {slope:.3f}x + {intercept:.3f}\nR^2 = {r_value**2:.3f}')

# Полиномиальная модель (2-го порядка)
coeffs = np.polyfit(x, y, 2)
poly = np.poly1d(coeffs)
x_poly = np.linspace(x.min(), x.max(), 100)
y_poly = poly(x_poly)
axs[0, 1].scatter(x, y)
axs[0, 1].plot(x_poly, y_poly, color='r')
axs[0, 1].set_title('Полиномиальная модель')
r2_poly = 1 - (sum((y - poly(x))**2) / ((len(y) - 1) * np.var(y, ddof=1)))
add_text(axs[0, 1], f'y = {coeffs[0]:.3f}x^2 + {coeffs[1]:.3f}x + {coeffs[2]:.3f}\nR^2 = {r2_poly:.3f}')

# Степенная модель
log_x = np.log(x)
log_y = np.log(y)
slope_pow, intercept_pow, r_value_pow, p_value, std_err = stats.linregress(log_x, log_y)
power_func = lambda x: np.exp(intercept_pow) * x**slope_pow
axs[1, 0].scatter(x, y)
axs[1, 0].plot(x, power_func(x), color='r')
axs[1, 0].set_title('Степенная модель')
add_text(axs[1, 0], f'y = {np.exp(intercept_pow):.4f}x^{slope_pow:.3f}\nR^2 = {r_value_pow**2:.3f}')

# Логарифмическая модель
log_x = np.log(x)
slope_log, intercept_log, r_value_log, p_value, std_err = stats.linregress(log_x, y)
log_func = lambda x: slope_log * np.log(x) + intercept_log
axs[1, 1].scatter(x, y)
axs[1, 1].plot(x, log_func(x), color='r')
axs[1, 1].set_title('Логарифмическая модель')
add_text(axs[1, 1], f'y = {slope_log:.3f}ln(x) + {intercept_log:.3f}\nR^2 = {r_value_log**2:.3f}')

for ax in axs.flat:
    ax.set(xlabel='Pb в воде', ylabel='Pb в волосах')

plt.tight_layout()
plt.show()

# Определение лучшей модели
r2 = {
    'Линейная': r_value**2,
    'Полиномиальная': r2_poly,
    'Степенная': r_value_pow**2,
    'Логарифмическая': r_value_log**2
}

best_model = max(r2, key=r2.get)
print(f"Лучшая модель: {best_model} (R^2 = {r2[best_model]:.3f})")
