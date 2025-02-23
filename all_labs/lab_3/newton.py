import math
import numpy as np
from scipy.optimize import newton as scipy_newton
import matplotlib.pyplot as plt
from all_labs.lab_3.my_func import f, f_prime, f_prime_prime
from io import BytesIO
import base64

def find_critical_points(start, end, step=1.0):
    critical_points = []
    x = start
    while x <= end:
        try:
            cp = scipy_newton(f_prime, x, tol=1e-6, maxiter=100)

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
    return "Локальный минимум" if f_prime_prime(cp) > 0 else "Локальный максимум"

def newton(start_range=-100, end_range=100):
    critical_points = find_critical_points(start_range, end_range)
    results = [{"x": round(cp, 4), "y": round(f(cp), 4), "type": classify_critical_point(cp)} for cp in critical_points]

    x_values = np.linspace(start_range, end_range, 500)
    x_values_filtered = [x for x in x_values if abs(1 + np.sin(x)) > 1e-3]
    y_values = [f(x) for x in x_values_filtered]

    plt.figure(figsize=(10, 6))
    plt.plot(x_values_filtered, y_values, label='f(x)')

    for cp in critical_points:
        plt.plot(cp, f(cp), 'go' if classify_critical_point(cp) == "Локальный минимум" else 'ro')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.legend()
    plt.ylim(-10, 25)
    plt.xlim(-25, 50)

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close()

    return {"critical_points": results, "image_base64": img_base64}