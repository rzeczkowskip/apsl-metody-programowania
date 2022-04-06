from typing import Callable, List


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


def menu(label: str, options: List[MenuLabel], redraw: bool = True) -> None:
    print(f"\n{label}\n")

    choices = [MenuItem('Zamknięcie menu', menu_exit)]
    print("{key}. {label}".format(key=0, label="Zamknięcie menu"))

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
