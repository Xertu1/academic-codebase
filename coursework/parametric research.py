import numpy as np
import matplotlib.pyplot as plt
import os

params = {}
with open("params.txt") as f:
    for line in f:
        if '=' in line:
            key, val = line.strip().split('=', 1)
            params[key.strip()] = float(val.strip())

F     = params["F"]
mu    = params["mu"]
m0    = params["m0"]
v0    = params["v0"]
t_end = params["t_end"]
h     = params["h"]

def analytic_velocity(t):
    return (F * t + m0 * v0) / (m0 + mu * t)

def dv_dt(t, v):
    return (F - mu * v) / (m0 + mu * t)

def euler_method():
    n = int(np.ceil(t_end / h))
    t = np.linspace(0, n * h, n + 1)
    v = np.zeros(n + 1)
    v[0] = v0
    for i in range(n):
        v[i + 1] = v[i] + h * dv_dt(t[i], v[i])
    return t, v

def rk4_method():
    n = int(np.ceil(t_end / h))
    t = np.linspace(0, n * h, n + 1)
    v = np.zeros(n + 1)
    v[0] = v0
    for i in range(n):
        ti, vi = t[i], v[i]
        k1 = dv_dt(ti, vi)
        k2 = dv_dt(ti + h/2, vi + h*k1/2)
        k3 = dv_dt(ti + h/2, vi + h*k2/2)
        k4 = dv_dt(ti + h, vi + h*k3)
        v[i + 1] = vi + h * (k1 + 2*k2 + 2*k3 + k4) / 6
    return t, v


def main():
    global mu
    out_dir = "parametric research"
    os.makedirs(out_dir, exist_ok=True)

    # графики v(t)
    t_exact = np.linspace(0, t_end, 1000)
    v_exact = analytic_velocity(t_exact)
    t_e, v_e = euler_method()
    t_r, v_r = rk4_method()

    # np.savetxt(f"{out_dir}/analytic.txt", np.column_stack((t_exact, v_exact)), header="t v_exact", fmt="%.6f %.6f")
    # np.savetxt(f"{out_dir}/euler.txt",   np.column_stack((t_e, v_e)),      header="t v_euler", fmt="%.6f %.6f")
    # np.savetxt(f"{out_dir}/rk4.txt",     np.column_stack((t_r, v_r)),      header="t v_rk4",   fmt="%.6f %.6f")
    #
    # plt.figure()
    # plt.plot(t_exact, v_exact, 'k-',   label="Аналитическое")
    # plt.plot(t_e,      v_e,      'o--b', label="Эйлер")
    # plt.plot(t_r,      v_r,      's--g', label="RK4")
    # plt.xlabel("t, с")
    # plt.ylabel("v(t), м/с")
    # plt.title(f"Решения при μ = {mu}")
    # plt.legend()
    # plt.grid(True)
    # plt.savefig(f"{out_dir}/solution_all.png", dpi=300)

    mu_vals = np.linspace(mu*0.1, mu*1.5, 50)
    v_exact_end = []
    v_euler_end = []
    v_rk4_end   = []
    for mu_i in mu_vals:
        v_exact_end.append(analytic_velocity(t_end))
        mu = mu_i
        res = euler_method()
        ve = res[1]
        res2 = rk4_method()
        vr = res2[1]
        v_euler_end.append(ve[len(ve)-1])
        v_rk4_end.append(vr[-1])

    plt.figure()
    plt.plot(mu_vals, v_exact_end, 'k-',   label="Аналитическое решение")
    plt.plot(mu_vals, v_euler_end, 'o--b', label="Метод Эйлера",  zorder=1)
    plt.plot(mu_vals, v_rk4_end,   's--g', label="Метод Рунге-Кутта",  zorder=2, alpha=0.7)
    plt.xlabel("mu, кг/с")
    plt.ylabel("v конечное")
    plt.title("Зависимость v от mu")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{out_dir}/v_mu.png", dpi=300)

if __name__ == "__main__":
    main()
