import matplotlib.pyplot as plt
import numpy as np

from Lab3.task3 import mse, polynomial, fit


def main() -> None:
    x_values = [-0.9, 0.0, 0.9, 1.8, 2.7, 3.6]
    y_values = [-1.2689, 0.0, 1.2689, 2.6541, 4.4856, 9.9138]
    grid = np.linspace(x_values[0], x_values[-1], 400)

    plt.figure(figsize=(9, 5))
    plt.scatter(x_values, y_values, label='Исходные данные', zorder=4)
    for n in (1, 2, 3):
        a = fit(x_values, y_values, n)
        values = [polynomial(x, a) for x in grid]
        plt.plot(grid, values, label=f'P_{n}(x), MSE{n} = {mse(x_values, y_values, a):.9f}')

    plt.title('3.3. Метод наименьших квадратов')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
