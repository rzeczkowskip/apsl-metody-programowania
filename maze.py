import os
from enum import Enum
from typing import List, Tuple
import _helpers
import maze_helpers

MAZE_MIN_SIZE = 3
MAZE_CELL_WIDTH = 3


class Direction(Enum):
    UP = 1,
    DOWN = 2,
    LEFT = 3,
    RIGHT = 4

    def is_x(self):
        return self == Direction.UP or self == Direction.DOWN

    def get_modifier(self):
        return 1 if self == Direction.DOWN or self == Direction.RIGHT else -1


class Step:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def get_next_step(self, _dir: Direction):
        modifier = _dir.get_modifier()

        [x_diff, y_diff] = [0, 1] if _dir.is_x() else [1, 0]

        return Step(self._x + (x_diff * modifier), self._y + (y_diff * modifier))

    def is_valid(self) -> bool:
        return self._y >= 0 and self._x >= 0

    def matrix_values(self) -> Tuple[int, int]:
        return self._y + 1, self._x + 1

    def __eq__(self, other):
        if type(other) == tuple:
            [x, y] = other
        else:
            try:
                x = other.x
                y = other.y
            except Exception:
                [x, y] = None

        return self._x == x and self.y == y


class Maze:
    def __init__(self, maze: List[List[int]]):
        self._maze = maze
        self._y_max = len(maze) - 1
        self._x_max = len(maze[0]) - 1
        self._size = len(maze) * len(maze[0])

    @property
    def y(self) -> int:
        return self._y_max + 1

    @property
    def x(self) -> int:
        return self._x_max + 1

    def has_position(self, step: Step):
        return step.y <= self._y_max and step.x <= self._x_max

    def can_go(self, step: Step):
        return self.has_position(step) and self._maze[step.y][step.x] == 1

    def print(self, steps: [Step]) -> None:
        result = []

        for y, row in enumerate(self._maze):
            result_row = []

            for x, cell in enumerate(row):
                selected = (x, y) in steps
                value = None if not selected else str(steps.index((x, y)))
                result_row.append(self._cell_to_string(cell, selected, value))

            result.append(''.join(result_row))

        print("\n".join(result))

    @staticmethod
    def _cell_to_string(cell, selected: bool = False, value: str = None):
        if value is None:
            value = '•'

        value = value.center(3, ' ')

        if cell == 0 and selected is False:
            return f"{value}"

        color = _helpers.CliColors.bg.lightgrey if selected is False else _helpers.CliColors.bg.green
        return f"{color}{_helpers.CliColors.fg.black}{value}{_helpers.CliColors.reset}"


# the algo!
def find_exit(maze: Maze, starting_point: Step, exit_point: Step) -> [Step]:
    results = []

    def populate_results(step: Step, current_path: [Step]) -> [Step]:
        nonlocal exit_point

        current_path.append(step)

        for _dir in Direction:
            _next = step.get_next_step(_dir)

            if not _next.is_valid() or _next in current_path:
                continue

            if _next == exit_point:
                current_path.append(_next)
                results.append(current_path)

                return

            if maze.can_go(_next):
                populate_results(_next, current_path.copy())

    populate_results(starting_point, [])

    return results


def run():
    try:
        [terminal_columns, terminal_lines] = os.get_terminal_size()
        maze_max_columns = int((terminal_columns - 5) / MAZE_CELL_WIDTH)
        maze_max_rows = terminal_lines - 10
    except OSError:
        maze_max_columns = 10
        maze_max_rows = 10

    print("Budujemy labirynt :)")
    print()
    print("### LEGENDA ###")
    print("Białe pola labiryntu, to pola, po których można się poruszać.")
    print("Czarne pola labiryntu, to ściany.")
    print()
    input("Naciśnij enter, aby kontynuować")

    # get maze size
    rows = maze_helpers.read_single_int_value(
        f"Podaj ilość wierszy (od {MAZE_MIN_SIZE} do {maze_max_rows})", MAZE_MIN_SIZE, maze_max_rows
    )
    cols = maze_helpers.read_single_int_value(
        f"Podaj ilość kolumn (od {MAZE_MIN_SIZE} do {maze_max_columns})", MAZE_MIN_SIZE, maze_max_columns
    )

    print()

    # build maze
    maze_builder = maze_helpers.MazeBuilder(cols, rows)
    if maze_helpers.ask_yes_no("Czy chcesz wygenerować losowy labirynt?") is True:
        maze = None
        while maze is None:
            maze = maze_builder.random_maze()
            maze.print([])

            if not maze_helpers.ask_yes_no("Czy akceptujesz labirynt?"):
                maze = None
    else:
        print("\n\nPodaj wartości (0 lub 1) dla kolejnych pól labiryntu.\n\n")

        maze_steps = []
        maze_example = maze_builder.with_steps([])
        for y in range(0, rows):
            for x in range(0, cols):
                maze_example.print([Step(x, y)])
                if maze_helpers.read_single_int_value(f"Podaj wartość dla współrzędnych {y + 1},{x + 1}", 0, 1):
                    maze_steps.append((x, y))

                print()

        maze = maze_builder.with_steps(maze_steps)

    maze.print([])

    # get start/end points
    print()
    print("Podaj współrzędne startu")
    start_step = maze_helpers.get_point_in_maze(maze)

    print()
    print("Podaj współrzędne wyjścia")
    exit_step = maze_helpers.get_point_in_maze(maze)

    print()
    print("Twój labirynt:")
    maze.print([start_step, exit_step])

    print()
    input('Naciśnij enter, aby rozpocząć poszukiwanie wyjścia...')

    # go!
    results = find_exit(
        maze,
        start_step,
        exit_step
    )

    result_count = len(results)

    if result_count == 0:
        print("Nie znalazłem rozwiązań")
        maze.print([start_step, exit_step])
        return 1

    results.sort(key=len)

    print()
    print("Znalezione rozwiązania: {count}".format(count=result_count))

    print()
    print("Najkrótsza droga:")
    maze.print(results[0])
    maze_helpers.pretty_print_steps(results[0])

    input('Naciśnij enter, aby kontynuować')

    if result_count > 1:
        maze_helpers.ask_yes_no(f"Czy chcesz zobaczyć pozostałe rozwiązania {result_count - 1}?")
        for i, steps in enumerate(results[1:]):
            print(f"Wynik {i + 2} z {result_count}\n")
            maze.print(steps)
            maze_helpers.pretty_print_steps(results[0])

            print()
            input("Naciśnij enter, aby kontynuować")


if __name__ == '__main__':
    run()
