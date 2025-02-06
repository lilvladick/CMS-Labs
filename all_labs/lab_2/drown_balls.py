import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import io
import base64
import json

def model(y, t, m, g, rho_liquid, r, mu):
    v, h = y
    V = (4/3) * np.pi * r**3
    k1 = 6 * np.pi * mu * r

    F_gravity = m * g
    F_buoyancy = rho_liquid * V * g
    F_drag = k1 * v

    a = (F_gravity - F_buoyancy - np.sign(v) * F_drag) / m
    dhdt = -v
    dvdt = a

    return [dvdt, dhdt]

def drown_balls(json_params: str):
    params = json.loads(json_params)

    r = params.get("r", 0.15)
    g = params.get("g", 9.81)
    rho_ball = params.get("rho_ball", 1100)
    rho_liquid = params.get("rho_liquid", 680)
    mu = params.get("mu", 0.0006)
    h = params.get("h", 1.5)

    V = (4/3) * np.pi * r**3
    m = rho_ball * V

    T = 10
    dt = 0.01
    N = int(T / dt)

    time = np.linspace(0, T, N)
    y0 = [0, h]

    solution = odeint(model, y0, time, args=(m, g, rho_liquid, r, mu))

    v = solution[:, 0]
    h_arr = solution[:, 1]

    if np.any(h_arr <= 0):
        stop_idx = np.where(h_arr <= 0)[0][0]
        time = time[:stop_idx]
        v = v[:stop_idx]
        h_arr = h_arr[:stop_idx]

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(time, v, label='Скорость')
    plt.xlabel('Время, с')
    plt.ylabel('Скорость, м/с')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(time, h_arr, label='Высота', color='r')
    plt.xlabel('Время, с')
    plt.ylabel('Высота, м')
    plt.legend()

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return {"image_url": f"data:image/png;base64,{img_b64}"}

if __name__ == '__main__':
    test_json = json.dumps({
        "r": 0.15,
        "g": 9.81,
        "rho_ball": 1100,
        "rho_liquid": 680,
        "mu": 0.0006,
        "h": 1.5
    })

    print(drown_balls(test_json))
