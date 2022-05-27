from typing import Callable, List, Optional


class CliColors:
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'


class Validator:
    @staticmethod
    def ValidateInt(number, _min: Optional[int]) -> int:
        try:
            number = int(number)

            if _min is not None and number < _min:
                raise ValueError

            return number
        except ValueError:
            raise ValidationError(
                "Podane wartości muszą być liczbami naturalnymi{greater_than}".format(
                    greater_than=" większymi od {min}. Od początku!".format(min=_min) if _min else ""
                )
            )


class MenuLabel:
    def __init__(self, label: str):
        self.label = label


class MenuItem(MenuLabel):
    def __init__(self, label: str, action: Callable[[], None]):
        super().__init__(label)
        self.action = action


class ValidationError(Exception):
    def __init__(self, message: str):
        self.message = message


def menu_exit() -> None:
    print('Wychodzę')


def menu(label: str, options: List[MenuLabel], redraw: bool = True, close_label: str = "Zamknięcie menu") -> None:
    print(f"\n{label}\n")

    choices = [MenuItem(close_label, menu_exit)]
    print("{key}. {label}".format(key=0, label=close_label))

    i = 1
    for option in options:
        if isinstance(option, MenuItem):
            print("{key}. {label}".format(key=i, label=option.label))
            choices.append(option)
            i += 1
        else:
            print("\n## {label}\n".format(label=option.label))

    print("\n")

    item_to_run = None
    while item_to_run is None:
        try:
            selected_option = int(input("Wybierz opcję: "))
            item_to_run = choices[selected_option]
        except (ValueError, IndexError):
            print("Błędna opcja.")

    print("\n# Wybrana opcja: {option}\n\n-------------\n".format(option=item_to_run.label))

    item_to_run.action()

    if redraw and item_to_run.action != menu_exit:
        input("\nNaciśnij [Enter], aby wrócić do poprzedniego menu\n")

        menu(label, options)
