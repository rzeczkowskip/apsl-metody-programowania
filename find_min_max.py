import random
import time
from typing import Callable, Optional, List
import _helpers


class Debug:
    def __init__(self):
        self.comparisons = 0
        self.changes = 0
        self.stopwatch_start_time = None

    def stopwatch_start(self) -> None:
        self.stopwatch_start_time = time.perf_counter()

    def stopwatch_stop(self) -> int:
        if self.stopwatch_start_time is None:
            raise RuntimeError('Stopwatch is not running')

        result = round(time.perf_counter() - self.stopwatch_start_time, 2)
        self.stopwatch_start_time = None

        return result

    def add_comparisons(self, count: int) -> None:
        self.comparisons += count

    def add_changes(self, count: int = 1) -> None:
        self.changes += count

    def calculate_big_o(self, items_count: int) -> float:
        return round(self.comparisons / items_count, 5)


def _parse_input(number, _min: Optional[int]) -> int:
    try:
        number = int(number)

        if _min is not None and number < _min:
            raise ValueError

        return number
    except ValueError:
        raise _helpers.ValidationError(
            "Podane wartości muszą być liczbami naturalnymi większymi od {min}. Od początku!".format(min=_min)
        )


def _random_number_list(count: int, _max: int) -> List[int]:
    if count < 1:
        raise ValueError("The random number list has to be 1 or larger")

    items = []

    for i in range(count):
        items.append(random.randint(0, _max))

    return items


def min_max_linear(seq: List[int], debug: Debug) -> List[int]:
    # can use seq[0] for _min and _max
    # then, we remove 2 comparisons from the loop (for i in seq[1:])
    _min = float('inf')
    _max = float('-inf')

    for i in seq:
        if i < _min:
            _min = i
            debug.add_changes()

        if i > _max:
            _max = i
            debug.add_changes()

        debug.add_comparisons(2)

    return [_min, _max]


def min_max_iterative(seq: List[int], debug: Debug) -> List[int]:
    seq_length = len(seq)

    if seq_length == 1:
        return [seq[0], seq[0]]

    if seq[0] < seq[1]:
        _min = seq[0]
        _max = seq[1]
    else:
        _min = seq[1]
        _max = seq[0]

    debug.add_comparisons(1)
    debug.add_changes(1)

    # can do this instead:
    # _min = seq[0]
    # _max = seq[0]
    # for i in range(1, seq_length - 1, 2)

    for i in range(2, seq_length - 1, 2):
        a = seq[i]
        b = seq[i + 1]

        if a < b:
            if a < _min:
                _min = a
                debug.add_changes()

            if b > _max:
                _max = b
                debug.add_changes()
        else:
            if b < _min:
                _min = b
                debug.add_changes()

            if a > _max:
                _max = a
                debug.add_changes()

        debug.add_comparisons(3)

    if seq_length % 2 != 0:
        a = seq[seq_length - 1]

        if a < _min:
            _min = a
            debug.add_changes()

        if a > _max:
            _max = a
            debug.add_changes()

        debug.add_comparisons(2)

    return [_min, _max]


def min_max_recursive(seq: List[int], debug: Debug) -> List[int]:
    seq_length = len(seq)

    if seq_length == 1:
        return [seq[0], seq[0]]

    if seq_length == 2:
        debug.add_comparisons(1)

        if seq[0] < seq[1]:
            return [seq[0], seq[1]]  # can return seq directly
        else:
            return [seq[1], seq[0]]  # can use seq.reverse() and return it directly

    mid = int(seq_length / 2)
    left = min_max_recursive(seq[0:mid], debug)
    right = min_max_recursive(seq[mid:], debug)

    if left[0] < right[0]:
        _min = left[0]
    else:
        _min = right[0]

    if left[1] > right[1]:
        _max = left[1]
    else:
        _max = right[1]

    debug.add_comparisons(2)
    debug.add_changes(1)

    return [_min, _max]


def select_algorithm_menu() -> Optional[Callable[[List[int], Debug], List[int]]]:
    selected_method = None

    def set_method_iterative():
        nonlocal selected_method
        selected_method = min_max_iterative

    def set_method_recursive():
        nonlocal selected_method
        selected_method = min_max_recursive

    def set_method_linear():
        nonlocal selected_method
        selected_method = min_max_linear

    _helpers.menu('Wybierz typ alogrytmu', [
        _helpers.MenuItem('Algorytm iteracyjny', set_method_iterative),
        _helpers.MenuItem('Algorytm rekurencyjny', set_method_recursive),
        _helpers.MenuItem('[BONUS] Algorytm liniowy', set_method_linear),
    ], redraw=False)

    return selected_method


def run() -> None:
    max_number = None
    seq_items_count = None

    print("Wyszukiwanie najmniejszego oraz największego wyrazu ciągu")

    algorithm_method = select_algorithm_menu()

    if algorithm_method is None:
        print("Nie wybrano typu algorytmu.")
        return

    while max_number is None or seq_items_count is None:
        try:
            max_number = _parse_input(input("Podaj wartość największego wyrazu ciągu: "), -1)
            seq_items_count = _parse_input(input("Podaj ilość wyrazów ciągu: "), 0)
        except _helpers.ValidationError as e:
            max_number = None
            seq_items_count = None
            print(e.message)

    seq = _random_number_list(seq_items_count, max_number)
    debug = Debug()
    debug_time = 0

    if seq_items_count > 1:
        debug.stopwatch_start()
        [_min, _max] = algorithm_method(seq, debug)
        debug_time = debug.stopwatch_stop()
    else:
        _min = seq[0]
        _max = seq[0]

    print("\n##############\n### Wyniki ###\n##############\n")

    print("Długość ciągu: {length}".format(length=seq_items_count))
    print("Czas wykonania algorytmu w sekundach: {time}".format(time=debug_time))
    print("Ilość zmian min/max: {changes}. Ilość porównań: {comparisons}.".format(
        changes=debug.changes,
        comparisons=debug.comparisons,
    ))

    big_o = debug.calculate_big_o(seq_items_count)
    print("Złożoność: O({big_o}n), co daje O({big_o_calculated})".format(
        big_o=big_o,
        big_o_calculated=big_o * seq_items_count
    ))

    print("Wartość minimalna: {min}. Wartość maksymalna: {max}".format(min=_min, max=_max))

    def draw_seq() -> None:
        nonlocal seq

        print("Ciąg wykorzystany do obliczeń:\n{seq}".format(seq=seq))

    _helpers.menu('Czy chcesz zobaczyć ciąg?', [
        _helpers.MenuItem('Pokaż ciąg liczb użyty do obliczeń', draw_seq),
    ], redraw=False)


if __name__ == '__main__':
    run()
