from typing import Callable

import _helpers
import euklides


def _parse_input(number) -> int:
    try:
        number = int(number)
        return number
    except ValueError:
        raise _helpers.ValidationError("Podane wartości muszą być liczbami naturalnymi większymi od zera. Od początku!")


def _validate_denominator(number: int) -> None:
    if number == 0:
        raise _helpers.ValidationError("Mianownik nie może być równy 0.")


class Fraction:
    def __init__(self, nominator: int, denominator: int):
        if denominator == 0:
            raise ZeroDivisionError

        self.nominator = nominator
        self.denominator = denominator

        self.nominator_abs = abs(nominator)
        self.denominator_abs = abs(denominator)

    def shorten(self, euklides_method: Callable[[int, int], int]):  # should return self
        if self.nominator == 0:
            return Fraction(self.nominator, self.denominator)

        nwd = euklides_method(self.nominator_abs, self.denominator_abs)
        return Fraction(int(self.nominator / nwd), int(self.denominator / nwd))

    def format_result_text(self) -> str:
        if self.nominator == 0:
            return "0"

        result = "{a}/{b}".format(a=self.nominator_abs, b=self.denominator_abs)

        if self.nominator * self.denominator < 0:
            return f"-({result})"

        return result


def run():
    nominator = None
    denominator = None

    euklides_method = euklides.select_algorithm_menu()
    if euklides_method is None:
        print("Nie wybrano metody obliczeń.")
        return

    while nominator is None or denominator is None:
        try:
            nominator = _parse_input(input("Podaj licznik: "))
            denominator = _parse_input(input("Podaj mianownik: "))
            _validate_denominator(denominator)
        except _helpers.ValidationError as e:
            nominator = None
            denominator = None

            print(e.message)

    fraction = Fraction(nominator, denominator)
    shortened_fraction = fraction.shorten(euklides_method)

    print("Skrócony ułamek {fraction} to {result}\n".format(
        fraction=fraction.format_result_text(),
        result=shortened_fraction.format_result_text()
    ))


if __name__ == '__main__':
    run()
