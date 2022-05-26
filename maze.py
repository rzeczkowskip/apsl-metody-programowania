from enum import Enum
from typing import List, Tuple


class Direction(Enum):
    UP = 1,
    DOWN = 2,
    LEFT = 3,
    RIGHT = 4

    def is_x(self):
        return self == Direction.UP or self == Direction.DOWN


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
        modifier = 1 if _dir == Direction.DOWN or _dir == Direction.RIGHT else -1

        [x_diff, y_diff] = [0, 1] if _dir.is_x() else [1, 0]

        return Step(self._x + (x_diff * modifier), self._y + (y_diff * modifier))

    def is_valid(self) -> bool:
        return self._y >= 0 and self._x >= 0

    def matrix_values(self) -> Tuple[int, int]:
        return self._y + 1, self._x + 1

    def __eq__(self, other):
        return type(other) == Step and self._x == other.x and self.y == other.y


class Maze:
    def __init__(self, maze: List[List[int]]):
        self._maze = maze
        self._y_max = len(maze) - 1
        self._x_max = len(maze[0]) - 1
        self._size = len(maze) * len(maze[0])

    def has_position(self, step: Step):
        return step.y <= self._y_max and step.x <= self._x_max

    def can_go(self, step: Step):
        return self.has_position(step) and self._maze[step.y][step.x] == 1


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

    # if exit_point.name() not in steps:
    #     return []

    return results


def print_result(maze: Maze, result: [Step]) -> None:
    pass


def run():
    exit_step = Step(4 - 1, 5 - 1)
    res = find_exit(
        Maze([
            [1, 1, 1, 0, 1, 0],
            [0, 1, 1, 1, 0, 1],
            [1, 1, 0, 1, 0, 1],
            [0, 1, 1, 1, 0, 1],
            [1, 0, 0, 1, 0, 1]
        ]),
        Step(2 - 1, 2 - 1),
        exit_step
    )

    res.sort(key=len)

    if len(res) == 0:
        print("Nie znalazłem rozwiązań")
        return 1

    print("Znalezione rozwiązania: {count}".format(count=len(res)))

    for steps in res:
        print(list(map(lambda step: step.matrix_values(), steps)))


if __name__ == '__main__':
    run()
