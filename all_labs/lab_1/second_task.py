import base64
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from scipy.optimize import curve_fit

def get_trends(data):
    data = pd.read_csv(data)
    data['date'] = pd.to_datetime(data['date'], format='%d.%m.%Y')

    data['x'] = (data['date'] - data['date'].min()).dt.days
    x = data['x'].values
    y = data['value'].values

    def linear(x, a, b): return a * x + b
    def polynomial(x, a, b, c): return a * x**2 + b * x + c
    def logarithmic(x, a, b): return a * np.log(x + 1) + b
    def exponential(x, a, b): return a * np.exp(b * x)

    lin_params, _ = curve_fit(linear, x, y)
    poly_params, _ = curve_fit(polynomial, x, y)
    log_params, _ = curve_fit(logarithmic, x, y)
    exp_params, _ = curve_fit(exponential, x, y)

    y_linear = linear(x, *lin_params)
    y_poly = polynomial(x, *poly_params)
    y_log = logarithmic(x, *log_params)
    y_exp = exponential(x, *exp_params)

    r2_lin = r2_score(y, y_linear)
    r2_poly = r2_score(y, y_poly)
    r2_log = r2_score(y, y_log)
    r2_exp = r2_score(y, y_exp)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    models = [
        (y_linear, lin_params, r2_lin, "Линейная"),
        (y_poly, poly_params, r2_poly, "Полиномиальная"),
        (y_log, log_params, r2_log, "Логаритмическая"),
        (y_exp, exp_params, r2_exp, "Экспоненциальная"),
    ]

    for ax, (y_pred, params, r2, label) in zip(axes.flat, models):
        ax.scatter(x, y, label="Данные", color="blue")
        ax.plot(x, y_pred, label=f"{label} линия тренда", color="red")
        ax.set_title(f"{label} модель: $R^2={r2:.4f}$")
        ax.legend()

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return {"image_url": f"data:image/png;base64,{img_b64}"}
