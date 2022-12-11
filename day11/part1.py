from __future__ import annotations

import argparse
from collections import deque
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

OPERATIONS = {"*": lambda a, b: a * b, "+": lambda a, b: a + b}


def compute(s: str) -> int:
    monkeys = s.split("\n\n")
    monkey_counts = [0 for _ in range(len(monkeys))]

    starting_items: list[deque[int]] = [deque() for _ in range(len(monkeys))]
    for idx, monkey in enumerate(monkeys):
        parts = monkey.splitlines()
        items = re.findall("[0-9]+", parts[1])
        for item_s in items:
            item = int(item_s)
            starting_items[idx].appendleft(item)

    for _ in range(20):
        for idx, monkey in enumerate(monkeys):
            parts = monkey.splitlines()
            operation_str = parts[2]
            after_equals = operation_str.split("=")[1]

            op = "*"
            if "+" in after_equals:
                op = "+"

            first_op, second_op = after_equals.split(op)
            test_number = int(re.findall("[0-9]+", parts[3])[0])
            true_monkey = int(re.findall("[0-9]+", parts[4])[0])
            false_monkey = int(re.findall("[0-9]+", parts[5])[0])

            def run_operation(item: int) -> int:
                first_n = second_n = 0
                if first_op.strip() == "old":
                    first_n = item
                else:
                    first_n = int(first_op)

                if second_op.strip() == "old":
                    second_n = item
                else:
                    second_n = int(second_op)

                return OPERATIONS[op](first_n, second_n)

            def handle_monkey(item: int) -> None:
                monkey_counts[idx] += 1
                worry_level = run_operation(item)
                worry_level //= 3
                if not worry_level % test_number:
                    to_monkey = true_monkey
                else:
                    to_monkey = false_monkey

                starting_items[to_monkey].appendleft(worry_level)

            while starting_items[idx]:
                item = starting_items[idx].pop()
                handle_monkey(item)

    monkey_counts.sort()
    return monkey_counts[-2] * monkey_counts[-1]


INPUT_S = """\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""
EXPECTED = 10605


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
