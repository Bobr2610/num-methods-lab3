from Lab1.task2 import sweep


def spline(
        x_values: list[float],
        y_values: list[float]
) -> list[tuple[float, float, float, float]]:
    n = len(x_values) - 1
    h = [x_values[i + 1] - x_values[i] for i in range(n)]

    c = [0.0] * (n + 1)
    if n > 1:
        lower = h[1:-1]
        diagonal = [2 * (h[i - 1] + h[i]) for i in range(1, n)]
        upper = h[1:-1]
        right = [
            3 * (
                (y_values[i + 1] - y_values[i]) / h[i]
                - (y_values[i] - y_values[i - 1]) / h[i - 1]
            )
            for i in range(1, n)
        ]

        if n == 2:
            c[1] = right[0] / diagonal[0]
        else:
            _, _, c[1:-1] = sweep(lower, diagonal, upper, right)

    coefficients = []
    for i in range(n):
        a = y_values[i]
        b = (y_values[i + 1] - y_values[i]) / h[i] - h[i] * (2 * c[i] + c[i + 1]) / 3
        d = (c[i + 1] - c[i]) / (3 * h[i])
        coefficients.append((a, b, c[i], d))

    return coefficients


def interval(
        x: float,
        x_values: list[float]
) -> int:
    for i in range(len(x_values) - 1):
        if x_values[i] <= x <= x_values[i + 1]:
            return i

    raise ValueError("Интервал сплайна не найден")


def value(
        x: float,
        x_values: list[float],
        coefficients: list[tuple[float, float, float, float]]
) -> float:
    i = interval(x, x_values)
    a, b, c, d = coefficients[i]
    dx = x - x_values[i]

    return a + b * dx + c * dx ** 2 + d * dx ** 3


def d2spline(
        x: float,
        x_values: list[float],
        coefficients: list[tuple[float, float, float, float]]
) -> float:
    i = interval(x, x_values)
    _, _, c, d = coefficients[i]

    return 2 * c + 6 * d * (x - x_values[i])


def main() -> None:
    x_values = [0.0, 0.9, 1.8, 2.7, 3.6]
    y_values = [0.0, 0.72235, 1.5609, 2.8459, 7.7275]
    x_test = 1.5

    coefficients = spline(x_values, y_values)
    S = value(x_test, x_values, coefficients)

    print("Исходные узлы и значения функции:")
    print(" i x_i y_i")
    for i, (x, y) in enumerate(zip(x_values, y_values)):
        print(f"{i}  {round(x, 9)}  {round(y, 9)}")

    print("\nКоэффициенты сплайна на каждом интервале:")
    print(" i [x_(i-1), x_i] a_i b_i c_i d_i")
    for i, (a, b, c, d) in enumerate(coefficients):
        print(
            f"{i + 1}  [{round(x_values[i], 9)}, {round(x_values[i + 1], 9)}]"
            f"  {round(a, 9)}  {round(b, 9)}  {round(c, 9)}  {round(d, 9)}"
        )

    print("S_i(x) = a_i + b_i(x - x_(i-1)) + c_i(x - x_(i-1))^2 + d_i(x - x_(i-1))^3")
    print(f"S({x_test}) = {round(S, 9)}")
    i = interval(x_test, x_values)
    print(f"Интервал, содержащий x*: {i + 1}, [{x_values[i]}, {x_values[i + 1]}]")

    eps = 1e-9
    print("\nПроверка прохождения сплайна через узлы:")
    print(" x_i y_i S(x_i) погрешность проверка")
    for x, y in zip(x_values, y_values):
        result = value(x, x_values, coefficients)
        error = abs(result - y)
        print(f"{round(x, 9)}  {round(y, 9)}  {round(result, 9)}  {error:.3e}  {'да' if error <= eps else 'нет'}")

    left = d2spline(x_values[0], x_values, coefficients)
    right = d2spline(x_values[-1], x_values, coefficients)
    print(f"S''(x_0) = {round(left, 9)}, граничное условие выполнено: {'да' if abs(left) <= eps else 'нет'}")
    print(f"S''(x_n) = {round(right, 9)}, граничное условие выполнено: {'да' if abs(right) <= eps else 'нет'}")

if __name__ == '__main__':
    main()
