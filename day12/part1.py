from __future__ import annotations

import argparse
from collections import deque
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def to_value(char: str) -> int:
    if char == "S":
        char = "a"
    elif char == "E":
        char = "z"
    return ord(char)


def compute(s: str) -> int:
    start_x = start_y = 0
    lines = s.splitlines()
    for x in range(len(lines)):
        for y in range(len(lines[0])):
            if lines[x][y] == "S":
                start_x = x
                start_y = y

    rows = len(lines)
    cols = len(lines[0])
    queue: deque[tuple[int, int, int]] = deque()
    queue.append((start_x, start_y, 0))
    seen = set()
    while queue:
        x, y, steps = queue.pop()
        if lines[x][y] == "E":
            # first to reach the end is quickest
            return steps
        elif (x, y) in seen:
            continue
        else:
            seen.add((x, y))
            char = lines[x][y]
            current_value = to_value(char)
            for next_x, next_y in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                if (
                    0 <= next_x < rows
                    and 0 <= next_y < cols
                    and (to_value(lines[next_x][next_y]) - current_value < 2)
                ):
                    queue.appendleft((next_x, next_y, steps + 1))

    return 0


INPUT_S = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""
EXPECTED = 31


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
