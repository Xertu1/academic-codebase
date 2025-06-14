import numpy as np
import matplotlib.pyplot as plt
import os

params = {}
with open("params.txt") as fp:
    for line in fp:
        key, val = line.split("=", 1)
        params[key.strip()] = float(val)

F      = params["F"]
mu     = params["mu"]
m0     = params["m0"]
v0     = params["v0"]
t_end  = params["t_end"]
h      = params["h"]

def analytic_velocity(t):
    return (F * t + m0 * v0) / (m0 + mu * t)

def dv_dt(t, v):
    return (F - mu * v) / (m0 + mu * t)


def euler_method():
    n = int(np.ceil(t_end / h))
    t = np.linspace(0, n * h, n + 1)
    v = np.zeros_like(t)
    v[0] = v0
    for i in range(n):
        v[i + 1] = v[i] + h * dv_dt(t[i], v[i])
    return t, v

def rk4_method():
    n = int(np.ceil(t_end / h))
    t = np.linspace(0, n * h, n + 1)
    v = np.zeros_like(t)
    v[0] = v0
    for i in range(n):
        k1 = dv_dt(t[i], v[i])
        k2 = dv_dt(t[i] + 0.5 * h, v[i] + 0.5 * h * k1)
        k3 = dv_dt(t[i] + 0.5 * h, v[i] + 0.5 * h * k2)
        k4 = dv_dt(t[i] + h,      v[i] + h * k3)
        v[i + 1] = v[i] + (h / 6) * (k1 + 2*k2 + 2*k3 + k4)
    return t, v

def main():
    t_full = np.linspace(0, t_end, 1000)
    v_full = analytic_velocity(t_full)

    t_e, v_e = euler_method()
    t_r, v_r = rk4_method()

    v_cut = analytic_velocity(t_e)

    h_str = str(int(h)) if float(h).is_integer() else str(h)

    base_dir   = "results"
    euler_dir  = os.path.join(base_dir, "euler_sol")
    rk4_dir    = os.path.join(base_dir, "rk4_sol")

    for d in (base_dir, euler_dir, rk4_dir):
        os.makedirs(d, exist_ok=True)

    # полное аналитическое
    np.savetxt(os.path.join(base_dir, f"analytic_full_{h_str}.txt"),
               np.column_stack((t_full, v_full)),
               header="t v_exact", fmt="%.6f %.10e")

    # обрезанное аналитическое
    cut_data = np.column_stack((t_e, v_cut))
    np.savetxt(os.path.join(euler_dir, f"analytic_cut_{h_str}.txt"),
               cut_data, header="t v_exact_cut", fmt="%.1f %.10e")
    np.savetxt(os.path.join(rk4_dir,   f"analytic_cut_{h_str}.txt"),
               cut_data, header="t v_exact_cut", fmt="%.1f %.10e")

    # численные решения
    np.savetxt(os.path.join(euler_dir, f"euler_{h_str}.txt"),
               np.column_stack((t_e, v_e)), header="t v_euler", fmt="%.6f %.14e")
    np.savetxt(os.path.join(rk4_dir,   f"rk4_{h_str}.txt"),
               np.column_stack((t_r, v_r)), header="t v_rk4",  fmt="%.6f %.50e")

    plt.figure()
    plt.plot(t_full, v_full, 'k-', label="Аналитическое (1000 т.)")
    plt.plot(t_e,    v_e,    'o--b', label="Эйлер")
    plt.plot(t_r,    v_r,    's--g', label="Рунге–Кутта")
    plt.xlabel("t, s")
    plt.ylabel("v(t), m/s")
    plt.title(f"Сравнение решений (h = {h})")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(base_dir, f"solutions_all_{h_str}.png"), dpi=300)
    plt.close()

if __name__ == "__main__":
    main()
