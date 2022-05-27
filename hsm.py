import re


class PinGeneratorError(Exception):
    def __init__(self, message: str):
        self.message = message


class PinGenerator:
    _regex = re.compile(r'(?i)^(?:[\da-f] ?){16}$')

    def __init__(self, converter: [int]):
        converter_len = len(converter)

        if converter_len != 16:
            raise PinGeneratorError("Tablica konwersji musi zawierać 16 elementów")

        for x in converter:
            if x < 0 or x > 9:
                raise PinGeneratorError("Tablica konwersji może zawierać tylko wartości od 0 do 9")

        self._converter = converter

    def validate_number(self, card_number: str) -> bool:
        return self._regex.match(card_number) is not None

    def get_pin(self, card_number: str) -> str:
        if not self.validate_number(card_number):
            raise PinGeneratorError('Niepoprawny zaszyfrowany numer karty.')

        digits = []
        for x in card_number.replace(" ", "")[0:4]:
            index = int(x, 16)

            digits.append(str(self._converter[index]))

        return ''.join(digits)


def run():
    generator = PinGenerator([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5])

    card_number = None
    while card_number is None:
        card_number = input("Podaj zaszyfrowany numer karty\n16 znaków, dozwolone znaki: 0-9, A-F, spacja: ")

        if not generator.validate_number(card_number):
            card_number = None
            print("Niepoprawny zaszyfrowany numer karty.")
            print()

    pin = generator.get_pin(card_number)

    print(f"Twój PIN: {pin}")


if __name__ == '__main__':
    run()
