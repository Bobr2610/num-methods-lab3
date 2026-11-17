from Lab1.task1 import lu, gauss


def normal(
        x_values: list[float],
        y_values: list[float],
        n: int
) -> tuple[list[list[float]], list[float]]:
    A = [
        [sum(x ** (k + i) for x in x_values) for i in range(n + 1)]
        for k in range(n + 1)
    ]
    b = [
        sum(y * x ** k for x, y in zip(x_values, y_values))
        for k in range(n + 1)
    ]

    return A, b


def fit(
        x_values: list[float],
        y_values: list[float],
        n: int
) -> list[float]:
    A, b = normal(x_values, y_values, n)
    L, U, P, _ = lu(A)
    a = gauss(P, L, U, b)

    return a


def polynomial(
        x: float,
        a: list[float]
) -> float:
    result = 0
    for i in range(len(a) - 1, -1, -1):
        result = result * x + a[i]

    return result


def squared_error(
        x_values: list[float],
        y_values: list[float],
        a: list[float]
) -> float:
    return sum((polynomial(x, a) - y) ** 2 for x, y in zip(x_values, y_values))


def mse(
        x_values: list[float],
        y_values: list[float],
        a: list[float]
) -> float:

    return squared_error(x_values, y_values, a) / len(x_values)


def main() -> None:
    x_values = [-0.9, 0.0, 0.9, 1.8, 2.7, 3.6]
    y_values = [-1.2689, 0.0, 1.2689, 2.6541, 4.4856, 9.9138]

    errors = []
    for n in (1, 2, 3):
        a = fit(x_values, y_values, n)

        print(f"\nСтепень многочлена: {n}")
        print("Коэффициенты:", [round(value, 9) for value in a])
        print(f"P_{n}(x) = " + " + ".join(f"{round(ai, 9)} * x^{i}" for i, ai in enumerate(a)))
        print(f"Сумма квадратов отклонений = {round(squared_error(x_values, y_values, a), 9)}")
        error = mse(x_values, y_values, a)
        errors.append(error)

    best = errors.index(min(errors)) + 1
    print("\nСравнение средних квадратов ошибок по всем исходным точкам:")
    for n, error in enumerate(errors, start=1):
        print(f"P_{n}: MSE{n} = {format(error, '.9f').rstrip('0').rstrip('.')}")
    print(f"Лучшее приближение по среднему квадрату ошибки: P_{best}(x), степень {best}")


if __name__ == '__main__':
    main()
