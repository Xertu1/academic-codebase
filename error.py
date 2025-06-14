import os
import numpy as np
import matplotlib.pyplot as plt

EULER_DIR = "results/euler_sol"
RK4_DIR = "results/rk4_sol"
EPS = 1e-30
err_dir = "errors"
os.makedirs(err_dir, exist_ok=True)

def load_cut_data(folder: str, prefix: str):
    numeric, analytic = {}, {}
    for fname in os.listdir(folder):
        if not fname.endswith(".txt"):
            continue
        path = os.path.join(folder, fname)
        stem = fname[:-4]
        parts = stem.split("_", 2)
        if parts[0] == prefix:
            h = float(parts[1])
            t, y = np.loadtxt(path).T
            numeric[h] = (t, y)
        elif parts[0] == "analytic" and parts[1] == "cut":
            h = float(parts[2])
            t, y = np.loadtxt(path).T
            analytic[h] = (t, y)
    if not numeric or not analytic:
        raise FileNotFoundError(f"missing files in {folder}")
    return numeric, analytic


def richardson(numeric):
    if len(numeric) < 3:
        return np.nan, np.nan
    h4, h2, h = sorted(numeric)[:3]

    y_h   = numeric[h][1]
    y_h2  = numeric[h2][1]
    y_h4  = numeric[h4][1]

    d1 = np.max(np.abs(y_h  - y_h2[::2]))
    d2 = np.max(np.abs(y_h2 - y_h4[::2]))

    if d2 < 1e-20:
        return np.nan, np.nan

    p   = np.log2((d1 + EPS)/(d2 + EPS))
    err = (d2 + EPS)/(2**p - 1)
    return p, err



def log_order_grid(numeric: dict):
    hs = sorted(numeric)
    logh, logr = [], []
    for j in range(1, len(hs)):
        h_big, h_small = hs[j], hs[j-1]            # 2:1
        if not np.isclose(h_big/h_small, 2.0):
            continue
        y_big   = numeric[h_big][1]
        y_small = numeric[h_small][1]
        resid = max(np.max(np.abs(y_big - y_small[::2])), EPS)
        logh.append(np.log(h_big))
        logr.append(np.log(resid))
    mask = np.array(logr) > np.log(EPS)+1e-12      # убираем EPS-точки
    if np.sum(mask) < 2:
        return np.nan
    k, _ = np.polyfit(np.array(logh)[mask], np.array(logr)[mask], 1)
    return -k



def plot_log_error(numeric, analytic, fname):
    logh, logr = [], []

    for h in sorted(numeric):
        t_n, y_n = numeric[h]
        t_e, y_e = analytic[h]


        r = np.max(np.abs(y_n - np.interp(t_n, t_e, y_e)))
        r = max(r, EPS)

        logh.append(np.log(h))
        logr.append(np.log(r))

    if len(logh) < 2:
        return

    plt.figure()
    plt.plot(logh, logr, "o-")
    plt.xlabel("log(h)")
    plt.ylabel("log(error)")
    plt.grid(True)
    plt.savefig(os.path.join(err_dir, fname), dpi=300)
    plt.close()



e_num, e_ex = load_cut_data(EULER_DIR, "euler")
r_num, r_ex = load_cut_data(RK4_DIR, "rk4")

p_e, err_e = richardson(e_num)
k_e = log_order_grid(e_num)

p_r, err_r = richardson(r_num)
k_r = log_order_grid(r_num)

print("Угловой коэффициент методом Эйлера:", round(k_e, 3))
print("Угловой коэффициент методом Рунге-Кутты:", round(k_r, 3))
print("Порядок точности для метода Эйлера:", round(p_e, 3))
print("Порядок точности для метода Рунге-Кутты:", round(p_r, 3))

plot_log_error(e_num, e_ex, "log(error) vs log(h) – Эйлер")
plot_log_error(r_num, r_ex, "log(error) vs log(h) – Рунге-Кутта")
