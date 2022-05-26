import math
from typing import List, Tuple

import _helpers


def _parse_input(number) -> float:
    try:
        number = float(number)

        if number is None or number < 0:
            raise ValueError

        return number
    except ValueError:
        raise _helpers.ValidationError(
            "Podane wartości muszą być liczbami rzeczywistymi większymi lub równymi 0. Od początku!"
        )


def get_lattice_points(r: float) -> List[Tuple[int, int]]:
    if r <= 0:
        return []

    r_int = math.ceil(r)

    result = [(0, 0)]

    for i in range(1, r_int):
        result.extend([(0, i), (i, 0), (0, -i), (-i, 0)])

    r_pow = r**2
    for x in range(1, r_int):
        x_pow = x**2
        y_pow_expected = r_pow - x_pow

        for y in range(1, r_int):
            if y**2 < y_pow_expected:
                result.extend([(x, y), (x, -y), (-x, y), (-x, -y)])

    return result


def count_lattice_points(r: float) -> int:
    if r <= 0:
        return 0

    r_int = math.ceil(r)
    result = (r_int - 1) * 4 + 1  # points on (0, 0), (+/- 1..r-1, 0) and (0, +/- 1..r-1) are always present

    r_pow = r**2
    for x in range(1, r_int):
        x_pow = x**2
        y_pow_max = r_pow - x_pow

        for y in range(1, r_int):
            if y**2 < y_pow_max:
                result += 4

    return result


def print_menu() -> bool:
    should_print = False

    def set_should_print_true():
        nonlocal should_print
        should_print = True

    _helpers.menu('Czy chcesz obliczyć i wypisać wszystkie punkty?', [
        _helpers.MenuItem('Tak', set_should_print_true),
    ], redraw=False)

    return should_print


def run() -> None:
    print("Punkty kratowe")

    r = None
    while r is None:
        try:
            r = _parse_input(input("Podaj promień okręgu (r): "))
        except _helpers.ValidationError as e:
            r = None
            print(e.message)

    points_count = count_lattice_points(r)
    print("\n##### WYNIK #####\n")
    print(f"Ilość punktów kratowych dla r={r} wynosi {points_count}")
    print()

    input("Naciśnij enter, aby kontynuować")

    if print_menu():
        print(get_lattice_points(r))


if __name__ == '__main__':
    run()
