import random
from typing import Optional, Tuple

import _helpers
from maze import Maze, Step


def ask_yes_no(message: str) -> bool:
    result = False

    def set_result_true():
        nonlocal result
        result = True

    _helpers.menu(message, [
        _helpers.MenuItem('Tak', set_result_true),
    ], redraw=False, close_label="Nie")

    return result


def _parse_input(number, _min: Optional[int] = None, _max: Optional[int] = None) -> int:
    try:
        number = int(number)

        if (_min is not None and number < _min) or (_max is not None and number > _max):
            raise ValueError

        return number
    except ValueError:
        raise _helpers.ValidationError(
            "Podane wartości muszą być liczbami całkowitymi od {min} do {max}. Jeszcze raz!".format(
                min="∞" if _min is None else _min,
                max="∞" if _max is None else _max,
            )
        )


def read_single_int_value(message: str, _min: Optional[int] = None, _max: Optional[int] = None):
    val = None

    while val is None:
        try:
            val = _parse_input(input(f"{message}: "), _min, _max)
        except _helpers.ValidationError as e:
            val = None
            print(e.message)

    return val


class MazeBuilder:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height

    def random_maze(self) -> Maze:
        steps = []

        for y in range(0, self._height):
            for x in range(0, self._width):
                if random.randint(0, 1) == 1:
                    steps.append((x, y))

        return self.with_steps(steps)

    def with_steps(self, steps: [Tuple[int, int]]) -> Maze:
        maze = []
        for y in range(0, self._height):
            row = []

            for x in range(0, self._width):
                row.append(1 if (x, y) in steps else 0)

            maze.append(row)

        return Maze(maze)


def get_point_in_maze(maze: Maze) -> Step:
    point = None
    while point is None:
        try:
            y = read_single_int_value(
                f"Podaj współrzędną wiersza (od 1 do {maze.y})",
                1,
                maze.y
            )

            x = read_single_int_value(
                f"Podaj współrzędną kolumny (od 1 do {maze.x})",
                1,
                maze.x
            )

            point = Step(x - 1, y - 1)
            if not maze.has_position(point):
                raise ValueError

        except ValueError:
            print(f"Podane współrzędne nie istnieją w labiryncie {point.matrix_values()}")
            point = None

    return point


def pretty_print_steps(steps: [Step]) -> None:
    print(' → '.join(list(map(lambda step: str(step.matrix_values()), steps))))