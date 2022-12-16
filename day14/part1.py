from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    cave = set()
    scans = s.splitlines()
    for scan in scans:
        inputs = [tuple(map(int, coords.split(","))) for coords in scan.split(" -> ")]
        for (ax, ay), (bx, by) in zip(inputs, inputs[1:]):
            if ax == bx:
                for dy in range(min(ay, by), max(ay, by) + 1):
                    cave.add((ax, dy))
            else:
                for dx in range(min(ax, bx), max(ax, bx) + 1):
                    cave.add((dx, ay))

    max_y = max(y for _, y in cave)

    count = 0
    while True:
        sand_x, sand_y = 500, 0
        while True:
            if (sand_x, sand_y + 1) not in cave:
                sand_y += 1
            elif (sand_x - 1, sand_y + 1) not in cave:
                sand_x -= 1
                sand_y += 1
            elif (sand_x + 1, sand_y + 1) not in cave:
                sand_x += 1
                sand_y += 1
            else:
                cave.add((sand_x, sand_y))
                break

            if sand_y > max_y:
                return count

        count += 1

    raise NotImplementedError()


INPUT_S = '''\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''
EXPECTED = 24


@pytest.mark.parametrize(

    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))


if __name__ == '__main__':
    raise SystemExit(main())
