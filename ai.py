import numpy as np
import matplotlib.pyplot as plt
import os

'''Комментарий обучающегося'''
# В финальной версии программы, представленной ниже, для повышения удобства, вручную незначительно изменена логика сохранения файлов.
# В частности добавлена возможность сохранения выходных данных в подкаталог results1 вместо корневой директории проекта
# и подкорректирован блок чтения параметров из файла, который так же изменен, и теперь един, для всей "экосистемы" программ,
# составляющих техническую часть курсовой работы.
# Помимо этого исправлено ОДУ для аналитического решений и добавлено начальное условие для получения корректных результатов.


def read_parameters(filename):
    """Чтение параметров из файла"""
    params = {}
    with open(filename, 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=')
                params[key.strip()] = float(value.strip())
    return params


def analytical_solution(t, F, m0, mu, v0):
    return (F * t + m0 * v0) / (m0 + mu * t)


def euler_method(F, m0, mu, t_end, h, v0):
    """Метод Эйлера"""
    t_values = np.arange(0, t_end + h, h)
    v_values = np.zeros_like(t_values)
    v_values[0] = v0

    for i in range(1, len(t_values)):
        t_prev = t_values[i - 1]
        v_prev = v_values[i - 1]
        m = m0 + mu * t_prev
        dvdt = (F - mu * v_prev) / m
        v_values[i] = v_prev + h * dvdt

    return t_values, v_values


def runge_kutta_4(F, m0, mu, t_end, h, v0):
    """Метод Рунге-Кутты 4-го порядка"""
    t_values = np.arange(0, t_end + h, h)
    v_values = np.zeros_like(t_values)
    v_values[0] = v0

    for i in range(1, len(t_values)):
        t_prev = t_values[i - 1]
        v_prev = v_values[i - 1]
        m = m0 + mu * t_prev

        # Вычисляем коэффициенты
        k1 = (F - mu * v_prev) / m
        k2 = (F - mu * (v_prev + 0.5 * h * k1)) / (m0 + mu * (t_prev + 0.5 * h))
        k3 = (F - mu * (v_prev + 0.5 * h * k2)) / (m0 + mu * (t_prev + 0.5 * h))
        k4 = (F - mu * (v_prev + h * k3)) / (m0 + mu * (t_prev + h))

        v_values[i] = v_prev + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

    return t_values, v_values


def save_results(filename, t_values, analytical, euler, rk4):
    """Сохранение результатов в файл"""
    with open(filename, 'w') as f:
        f.write("Time\tAnalytical\tEuler\tRunge-Kutta 4\n")
        for t, a, e, r in zip(t_values, analytical, euler, rk4):
            f.write(f"{t:.4f}\t{a:.6f}\t{e:.6f}\t{r:.6f}\n")


def main():
    # Чтение параметров из файла
    params = read_parameters('params.txt')
    F = params['F']
    m0 = params['m0']
    mu = params['mu']
    t_end = params['t_end']
    h = params['h']
    v0 = params['v0']

    # Вычисление решений
    t_values = np.arange(0, t_end + h, h)

    # Аналитическое решение
    v_analytical = analytical_solution(t_values, F, m0, mu, v0)

    # Численные решения
    t_euler, v_euler = euler_method(F, m0, mu, t_end, h, v0)
    t_rk4,   v_rk4   = runge_kutta_4(F, m0, mu, t_end, h, v0)



    if not os.path.exists("results1"):
        os.makedirs("results1")
    save_results('results1/results1_correct.txt', t_values, v_analytical, v_euler, v_rk4)

    # Визуализация (опционально)
    plt.plot(t_values, v_analytical, label='Analytical')
    plt.plot(t_euler, v_euler, '--', label='Euler')
    plt.plot(t_rk4, v_rk4, ':', label='Runge-Kutta 4')
    plt.xlabel('Time')
    plt.ylabel('Velocity')
    plt.legend()
    plt.grid()
    plt.savefig('results1/solution_plot_correct.png')
    plt.show()

if __name__ == "__main__":
    main()