def differences(
        x_values: list[float],
        y_values: list[float],
        i: int
) -> tuple[float, float, float]:

    first = (y_values[i + 1] - y_values[i]) / (x_values[i + 1] - x_values[i])
    second = (y_values[i + 2] - y_values[i + 1]) / (x_values[i + 2] - x_values[i + 1])
    difference = (second - first) / (x_values[i + 2] - x_values[i])

    return first, second, difference


def derivatives(
        x: float,
        x_values: list[float],
        y_values: list[float],
        i: int
) -> tuple[float, float]:
    first, _, difference = differences(x_values, y_values, i)

    df = first + difference * (2 * x - x_values[i] - x_values[i + 1])
    d2f = 2 * difference

    return df, d2f


def main() -> None:
    x_values = [1.0, 2.0, 3.0, 4.0, 5.0]
    y_values = [1.0, 2.6931, 4.0986, 5.3863, 6.6094]
    x_test = 3.0
    i = 1

    left, right, _ = differences(x_values, y_values, i)
    df, d2f = derivatives(x_test, x_values, y_values, i)

    print("Исходная таблица значений функции:")
    print(" i x_i y_i")
    for j, (x, y) in enumerate(zip(x_values, y_values)):
        print(f"{j}  {round(x, 9)}  {round(y, 9)}")
    print(f"x* = {x_test}")
    print("Индексы выбранных узлов:", list(range(i, i + 3)))
    print("Выбранные значения функции:", y_values[i:i + 3])
    print("Выбранные узлы:", x_values[i:i + 3])
    print(f"Наклон левой секущей: {round(left, 9)}")
    print(f"Наклон правой секущей: {round(right, 9)}")
    print(f"y'({x_test}) = {round(df, 9)}")
    print(f"y''({x_test}) = {round(d2f, 9)}")


if __name__ == '__main__':
    main()
