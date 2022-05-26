from typing import List, Callable


class MinMaxResult:
    def __init__(self, a: int, b: int, new_items: List[int]):
        self.a = a
        self.b = b
        self.items = new_items
        self.sum = a + b


def get_min(items: List[int]) -> MinMaxResult:
    _min = min(items)
    min_index = items.index(_min)

    items.pop(min_index)

    a = _min

    _min = min(items)
    min_index = items.index(_min)

    items.pop(min_index)

    return MinMaxResult(a, _min, items)


def get_max(items: List[int]) -> MinMaxResult:
    _max = max(items)
    min_index = items.index(_max)

    items.pop(min_index)

    a = _max

    _max = max(items)
    min_index = items.index(_max)

    items.pop(min_index)

    return MinMaxResult(a, _max, items)


def glue_numbers_iterative(numbers: List[int], callback: Callable[[List[int]], MinMaxResult]) -> None:
    cost = 0
    while len(numbers) > 1:
        min_max = callback(numbers)
        numbers.append(min_max.sum)

        cost += min_max.sum

    print("Suma: {sum}. Koszt: {cost}".format(sum=numbers[0], cost=cost))


def glue_numbers_recursive(numbers: List[int], callback: Callable[[List[int]], MinMaxResult]) -> None:
    class Result:
        def __init__(self, _sum: int, cost: int):
            self.sum = _sum
            self.cost = cost

    def glue(items: List[int], current_cost: int):
        _len = len(items)

        if _len == 1:
            return Result(items[0], current_cost)

        min_max = callback(items)
        min_max.items.append(min_max.sum)

        return glue(min_max.items, current_cost + min_max.sum)

    result = glue(numbers, 0)
    print("Suma: {sum}. Koszt: {cost}".format(sum=result.sum, cost=result.cost))


def run() -> None:
    print("Sklejanie par liczb")

    print("# Iteracyjnie")
    print()

    print("## Wybieramy minimalne")
    glue_numbers_iterative([1, 2, 3, 4, 5], get_min)
    print()

    print("## Wybieramy maksymalne")
    glue_numbers_iterative([1, 2, 3, 4, 5], get_max)
    print()

    print("# Rekurencyjnie")
    print()

    print("## Wybieramy minimalne")
    glue_numbers_recursive([1, 2, 3, 4, 5], get_min)
    print()

    print("## Wybieramy maksymalne")
    glue_numbers_recursive([1, 2, 3, 4, 5], get_max)
    print()


if __name__ == '__main__':
    run()
