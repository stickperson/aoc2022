from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def are_touching(x: tuple[int, int], y: tuple[int, int]) -> bool:
    return abs(x[0] - y[0]) < 2 and abs(x[1] - y[1]) < 2


DIRECTIONS = {"R": (0, 1), "L": (0, -1), "U": (1, 0), "D": (-1, 0)}


def compute(s: str) -> int:
    seen = set()
    tail = (0, 0)
    head = (0, 0)
    steps = s.splitlines()
    seen.add(tuple(tail))
    for step in steps:
        dir, num = step.split()
        direction_coords = DIRECTIONS[dir]
        previous_head = head
        for _ in range(int(num)):
            previous_head = tuple(head) # type: ignore
            new_head_x = head[0] + direction_coords[0]
            new_head_y = head[1] + direction_coords[1]
            head = (new_head_x, new_head_y)

            if not are_touching(head, tail):
                tail = previous_head

            seen.add(tuple(tail))
    return len(seen)


INPUT_S = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
U 4
"""
EXPECTED = 15


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
