from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


DIRECTIONS = {"R": (0, 1), "L": (0, -1), "U": (1, 0), "D": (-1, 0)}


def diff_to_move(x: int) -> int:
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0


def catch_up(leader: tuple[int, int], follower: tuple[int, int]) -> tuple[int, int]:
    leader_x_diff = leader[0] - follower[0]
    leader_y_diff = leader[1] - follower[1]

    if abs(leader_x_diff) > 1 or abs(leader_y_diff) > 1:
        new_x = follower[0] + diff_to_move(leader_x_diff)
        new_y = follower[1]+ diff_to_move(leader_y_diff)
        follower = new_x, new_y

    return follower


def compute(s: str) -> int:
    seen = set()
    steps = s.splitlines()

    knots = [(0, 0) for _ in range(10)]

    seen.add((0, 0))
    for step in steps:
        dir, num = step.split()
        for _ in range(int(num)):
            # Move the head
            diff = DIRECTIONS[dir]
            knots[0] = (knots[0][0] + diff[0], knots[0][1] + diff[1])

            # Catch the remaining knots up
            for idx in range(1, 10):
                tail = catch_up(knots[idx - 1], knots[idx])
                knots[idx] = tail

            seen.add(knots[-1])

    return len(seen)


INPUT_S = """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""
EXPECTED = 36


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
