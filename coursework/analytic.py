import sympy as sp
t, F, mu, m0, v0 = sp.symbols('t F mu m0 v0', positive=True, real=True)

v_expr = (F*t + v0*m0) / (m0 + mu*t)

v_func = sp.lambdify((t, F, mu, m0, v0), v_expr)

def analytic_velocity_at_t(t_val: float, F_val: float, mu_val: float, m0_val: float, v0_val: float) -> float:
    return float(v_func(t_val, F_val, mu_val, m0_val, v0_val))

if __name__ == "__main__":
    F_val   = 10.0
    mu_val  = 0.5
    m0_val  = 5.0
    v0_val  = 0.0
    t_const = 60.0

    v_at_const = analytic_velocity_at_t(t_const, F_val, mu_val, m0_val, v0_val)
    print(f"Скорость для t = {t_const:.2f} : {v_at_const:.6f} m/s")
