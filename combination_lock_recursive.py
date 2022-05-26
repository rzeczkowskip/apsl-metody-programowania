from typing import List


def count_enabled_bits(num: int) -> int:
    count = 0
    while num > 0:
        count += num & 1
        num = num >> 1

    return count


def are_most_significant_bits_valid(num: int, bits_count: int) -> bool:
    return num >> bits_count - 2 == 0b10


def generate_codes(bits_count: int, max_bits_count: int) -> List[int]:
    if bits_count > max_bits_count:
        return []

    code = 0b1 << (bits_count - 1)
    _max = (code << 1) - 1

    combinations = []

    while code <= _max:
        if not are_most_significant_bits_valid(code, bits_count):
            combinations.extend(generate_codes(bits_count + 1, max_bits_count))
            break

        if count_enabled_bits(code) % 2 == 0:
            combinations.append(code)

        code += 1

    return combinations


def run() -> None:
    min_bits = 2
    max_bits = 10

    combinations = generate_codes(min_bits, max_bits)

    combinations_in_row = 10

    print("Lista kodów do zamka szyfrowego spełniających następujące warunki:")
    print("Ilość kodów: {count}".format(count=len(combinations)))
    print()
    print("  1. Wartość bitu poprzedzającego najbardziej znaczący bit (pierwszy od lewej, zawsze równy 1) musi być równa 0.")
    print("  2. Suma wszystkich bitów musi być liczbą parzystą.")
    print("  3. Liczba bitów nie może być mniejsza niż dwa i większa niż dziesięć.")
    print()
    input("Naciśnij enter, aby zobaczyć listę")
    print()
    for i in range(0, len(combinations) + 1, 5):
        print('\t'.join(map(str, combinations[i:i + combinations_in_row])))


if __name__ == '__main__':
    run()
