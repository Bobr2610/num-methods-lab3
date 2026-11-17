from math import pi, tan

import matplotlib.pyplot as plt
import numpy as np

from Lab3.task1 import lagrange, divided_differences, newton


def main() -> None:
    x_values_a = [0, pi / 8, pi / 4, 3 * pi / 8]
    x_values_b = [0, pi / 8, pi / 3, 3 * pi / 8]
    x_test = 3 * pi / 16
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), sharey=True)

    for ax, (name, x_values) in zip(axes, (("А", x_values_a), ("Б", x_values_b))):
        y_values = [tan(x) + x for x in x_values]
        coefficients = divided_differences(x_values, y_values)
        grid = np.linspace(x_values[0], x_values[-1], 400)
        L_n = [lagrange(x, x_values, y_values) for x in grid]
        P_n = [newton(x, x_values, coefficients) for x in grid]

        ax.plot(grid, np.tan(grid) + grid, label='f(x) = tg(x) + x')
        ax.plot(grid, L_n, '--', label='L_3(x), Лагранж')
        ax.plot(grid, P_n, ':', label='P_3(x), Ньютон')
        ax.scatter(x_values, y_values, label='Узлы', zorder=4)
        ax.scatter([x_test], [tan(x_test) + x_test], marker='x', label='x*', zorder=5)
        ax.set_title(f'Набор узлов {name}')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(alpha=0.3)
        ax.legend()

    fig.suptitle('3.1. Интерполяция Лагранжа и Ньютона')
    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
