from math import atan, log, sqrt


def f(
        x: float
) -> float:
    return 1 / (x ** 4 + 16)


def nodes(
        a: float,
        b: float,
        h: float
) -> list[float]:

    n = round((b - a) / h)

    return [a + i * h for i in range(n)] + [b]


def left_rectangles(
        a: float,
        b: float,
        h: float
) -> float:
    x_values = nodes(a, b, h)
    F = 0
    for x in x_values[:-1]:
        F += h * f(x)

    return F


def right_rectangles(
        a: float,
        b: float,
        h: float
) -> float:
    x_values = nodes(a, b, h)
    F = 0
    for x in x_values[1:]:
        F += h * f(x)

    return F


def rectangles(
        a: float,
        b: float,
        h: float
) -> float:
    x_values = nodes(a, b, h)
    F = 0
    for i in range(1, len(x_values)):
        F += h * f((x_values[i - 1] + x_values[i]) / 2)

    return F


def trapezoids(
        a: float,
        b: float,
        h: float
) -> float:
    x_values = nodes(a, b, h)
    F = h * (f(a) + f(b)) / 2
    for x in x_values[1:-1]:
        F += h * f(x)

    return F


def simpson(
        a: float,
        b: float,
        h: float
) -> float:
    x_values = nodes(a, b, h)
    n = len(x_values) - 1

    F = f(a) + f(b)
    for i in range(1, n):
        F += (4 if i % 2 else 2) * f(x_values[i])

    return h * F / 3


def runge_romberg(
        F_h: float,
        F_kh: float,
        k: float,
        p: int
) -> tuple[float, float]:

    correction = (F_h - F_kh) / (k ** p - 1)
    F = F_h + correction
    R = abs(correction)

    return F, R


def antiderivative(
        x: float
) -> float:
    root2 = sqrt(2)
    return (
        log((x ** 2 + 2 * root2 * x + 4) / (x ** 2 - 2 * root2 * x + 4)) / (32 * root2)
        + (atan(x / root2 + 1) + atan(x / root2 - 1)) / (16 * root2)
    )


def main() -> None:
    a, b = 0.0, 2.0
    h1, h2 = 0.5, 0.25
    reference = antiderivative(b) - antiderivative(a)

    print(f"Интеграл функции 1/(x^4 + 16) на отрезке [{a}, {b}], h1 = {h1}, h2 = {h2}")
    print(f"Точное значение интеграла: {reference:.12f}")
    print(
        f"{'Метод':<24} {'F(h1)':>14} {'F(h2)':>14} {'p':>2} {'F(Рунге)':>14}"
        f" {'Оценка R(h2)':>13} {'Ошибка h1':>13} {'Ошибка h2':>13} {'Ошибка Рунге':>13}"
    )
    results = []
    for name, method, p in (
            ("Левые прямоугольники", left_rectangles, 1),
            ("Правые прямоугольники", right_rectangles, 1),
            ("Средние прямоугольники", rectangles, 2),
            ("Трапеции", trapezoids, 2),
            ("Симпсон", simpson, 4)
    ):
        F_kh = method(a, b, h1)
        F_h = method(a, b, h2)
        F, R = runge_romberg(F_h, F_kh, h1 / h2, p)
        error_h1 = abs(F_kh - reference)
        error_h2 = abs(F_h - reference)
        error_Runge = abs(F - reference)
        results.append((name, error_h1, error_h2, error_Runge))
        print(
            f"{name:<24} {F_kh:14.12f} {F_h:14.12f} {p:2} {F:14.12f}"
            f" {R:13.6e} {error_h1:13.6e} {error_h2:13.6e} {error_Runge:13.6e}"
        )

    for column, label in ((1, "h1"), (2, "h2"), (3, "Рунге–Ромберг")):
        best = results[0]
        for result in results[1:]:
            if result[column] < best[column]:
                best = result
        print(f"Наиболее точный метод ({label}): {best[0]}, погрешность = {best[column]:.6e}")


if __name__ == '__main__':
    main()
