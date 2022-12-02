from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


WINNING_MAP = {"A": "Y", "B": "Z", "C": "X"}
SCORES = {"X": 1, "Y": 2, "Z": 3}
DRAW = {"A": "X", "B": "Y", "C": "Z"}


def compute(s: str) -> int:
    games = s.splitlines()
    score = 0
    for game in games:
        opponent, me = game.split()
        score += SCORES[me]
        if WINNING_MAP.get(opponent) == me:
            score += 6
        elif DRAW[opponent] == me:
            score += 3
    return score


INPUT_S = """\
A Y
B X
C Z
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
