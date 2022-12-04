from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def contains(first_region, second_region):
    if (first_region[0] <= second_region[0]) and (first_region[1] >= second_region[0]):
        return True
    return False


def compute(s: str) -> int:
    section_pairs = s.splitlines()
    total = 0
    for pair in section_pairs:
        first_section, second_section = pair.split(",")
        first_section = first_section.split("-")
        second_section = second_section.split("-")
        first_start = int(first_section[0])
        first_end = int(first_section[1])

        second_start = int(second_section[0])
        second_end = int(second_section[1])
        if contains([first_start, first_end], [second_start, second_end]) or contains(
            [second_start, second_end], [first_start, first_end]
        ):
            total += 1
    return total


INPUT_S = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""
EXPECTED = 4


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
