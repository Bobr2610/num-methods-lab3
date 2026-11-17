from math import factorial, pi, prod, tan


def basis(
        x: float,
        i: int,
        x_values: list[float]
) -> float:
    result = 1

    for j in range(len(x_values)):
        if i == j:
            continue

        result *= (x - x_values[j]) / (x_values[i] - x_values[j])

    return result


def lagrange(
        x: float,
        x_values: list[float],
        y_values: list[float]
) -> float:
    result = 0

    for i in range(len(x_values)):
        result += y_values[i] * basis(x, i, x_values)

    return result


def divided_differences(
        x_values: list[float],
        y_values: list[float]
) -> list[float]:

    differences = y_values.copy()
    coefficients = [differences[0]]

    for order in range(1, len(x_values)):
        for i in range(len(x_values) - order):
            differences[i] = (differences[i + 1] - differences[i]) / (
                x_values[i + order] - x_values[i]
            )

        coefficients.append(differences[0])

    return coefficients


def newton(
        x: float,
        x_values: list[float],
        coefficients: list[float]
) -> float:
    result = coefficients[-1]
    for i in range(len(coefficients) - 2, -1, -1):
        result = coefficients[i] + (x - x_values[i]) * result

    return result


def d4f(
        x: float
) -> float:
    t = tan(x)
    return 8 * t * (1 + t ** 2) * (2 + 3 * t ** 2)


def max_d4f(
        x_values: list[float]
) -> float:
    a, b = min(x_values), max(x_values)
    # На заданном отрезке [0, 3*pi/8] четвёртая производная возрастает.
    return max(abs(d4f(a)), abs(d4f(b)))


def omega(
        x: float,
        x_values: list[float]
) -> float:
    result = 1

    for xi in x_values:
        result *= x - xi

    return result


def error_bound(
        x: float,
        x_values: list[float]
) -> float:
    return max_d4f(x_values + [x]) / factorial(4) * abs(omega(x, x_values))


def main() -> None:
    x_values_a = [0, pi / 8, pi / 4, 3 * pi / 8]
    x_values_b = [0, pi / 8, pi / 3, 3 * pi / 8]
    x_test = 3 * pi / 16
    actual = tan(x_test) + x_test

    for name, x_values in (("А", x_values_a), ("Б", x_values_b)):
        y_values = [tan(x) + x for x in x_values]
        count = len(x_values)

        table = [[None] * count for _ in range(count)]
        for i, y in enumerate(y_values):
            table[i][0] = y

        for order in range(1, count):
            for i in range(count - order):
                table[i][order] = (table[i + 1][order - 1] - table[i][order - 1]) / (
                    x_values[i + order] - x_values[i]
                )

        coefficients = divided_differences(x_values, y_values)
        L_n = lagrange(x_test, x_values, y_values)
        P_n = newton(x_test, x_values, coefficients)

        print(f"\nНабор узлов {name}")
        print("Исходные узлы и значения функции f(x) = tg(x) + x:")
        for i, (xi, yi) in enumerate(zip(x_values, y_values)):
            print(f"  x_{i} = {round(xi, 9)}, y_{i} = {round(yi, 9)}")

        lagrange_terms = []
        for i, yi in enumerate(y_values):
            denominator = prod(
                x_values[i] - x_values[j] for j in range(count) if j != i
            )
            factors = " * ".join(
                f"(x - {round(x_values[j], 9)})" for j in range(count) if j != i
            )
            lagrange_terms.append(f"{round(yi / denominator, 9)} * {factors}")

        print("\nМногочлен Лагранжа:")
        print("  L(x) = " + " + ".join(lagrange_terms))

        print("\nТаблица разделённых разностей:")
        print("i x_i [f[x_i], разности первого, второго и третьего порядков]")
        for i in range(count):
            row = [round(value, 9) for value in table[i] if value is not None]
            print(i, round(x_values[i], 9), row)

        newton_terms = [f"{round(coefficients[0], 9)}"]
        for order in range(1, count):
            factors = " * ".join(f"(x - {round(xi, 9)})" for xi in x_values[:order])
            newton_terms.append(f"{round(coefficients[order], 9)} * {factors}")

        print("\nМногочлен Ньютона:")
        print("  P(x) = " + " + ".join(newton_terms))

        print(f"\nx* = {round(x_test, 9)}:")
        print(f"  L(x*) = {round(L_n, 9)}")
        print(f"  P(x*) = {round(P_n, 9)}")
        print(f"  f(x*) = {round(actual, 9)}")
        print(f"  |f(x*) - L(x*)| = {round(abs(actual - L_n), 9)}")
        print(f"  |f(x*) - P(x*)| = {round(abs(actual - P_n), 9)}")
        print(f"  |L(x*) - P(x*)| = {round(abs(L_n - P_n), 9)}")
        print(f"  Верхняя оценка погрешности = {round(error_bound(x_test, x_values), 9)}")

if __name__ == "__main__":
    main()
