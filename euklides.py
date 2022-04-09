from typing import Callable, Optional
import _helpers


def nww(a: int, b: int, nwd_callback: Callable[[int, int], int]) -> int:
    return int(a * b / nwd_callback(a, b))


def nwd_mod_recursive(a: int, b: int) -> int:
    return a if b == 0 else nwd_mod_recursive(b, a % b)


def nwd_mod_iterative(a: int, b: int) -> int:
    while b > 0:
        c = a % b
        a = b
        b = c

    return a


def nwd_minus_recursive(a: int, b: int) -> int:
    if a > b:
        return nwd_minus_recursive(a - b, b)

    if a < b:
        return nwd_minus_recursive(a, b - a)

    return a


def nwd_minus_iterative(a: int, b: int) -> int:
    while a != b:
        if a > b:
            a = a - b
        if b > a:
            b = b - a

    return a


def _parse_input(number) -> int:
    try:
        number = int(number)

        if number < 0:
            raise ValueError

        return number
    except ValueError:
        raise _helpers.ValidationError("Podane wartości muszą być liczbami naturalnymi większymi od zera. Od początku!")


def select_algorithm_menu() -> Optional[Callable[[int, int], int]]:
    nwd_method = None

    def set_nwd_mod_recursive():
        nonlocal nwd_method
        nwd_method = nwd_mod_recursive

    def set_nwd_mod_iterative():
        nonlocal nwd_method
        nwd_method = nwd_mod_iterative

    def set_nwd_minus_recursive():
        nonlocal nwd_method
        nwd_method = nwd_minus_recursive

    def set_nwd_minus_iterative():
        nonlocal nwd_method
        nwd_method = nwd_minus_iterative

    _helpers.menu('Wybierz metodę obliczeń największego wspólnego dzielnika (NWD)', [
        _helpers.MenuItem('Modulo rekurencyjnie', set_nwd_mod_recursive),
        _helpers.MenuItem('Modulo iteracyjnie', set_nwd_mod_iterative),
        _helpers.MenuItem('Odejmowanie rekurencyjnie', set_nwd_minus_recursive),
        _helpers.MenuItem('Odejmowanie iteracyjnie', set_nwd_minus_iterative),
    ], redraw=False)

    return nwd_method


def run():
    a = None
    b = None

    print("Oblicznie najmniejszej wspólnej wielokrotności (NWW) dwóch liczb naturalnych a i b:")

    nwd_method = select_algorithm_menu()

    if nwd_method is None:
        print("Nie wybrano metody obliczeń.")
        return

    while a is None or b is None:
        try:
            a = _parse_input(input("Podaj a: "))
            b = _parse_input(input("Podaj b: "))
        except _helpers.ValidationError as e:
            a = None
            b = None
            print(e.message)

    print("Największy wspólny dzielnik dla {a} i {b} wynosi {result}".format(a=a, b=b, result=nwd_method(a, b)))
    print("Najmniejsza wspólna wielokrotność dla {a} i {b} wynosi {result}\n".format(
        a=a,
        b=b,
        result=nww(a, b, nwd_method)
    ))


if __name__ == '__main__':
    run()
