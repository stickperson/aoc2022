from __future__ import annotations

import argparse
from functools import reduce
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    scenic_score = 0
    lines = s.splitlines()
    rows = len(lines)
    cols = len(lines[0])
    for row_idx in range(1, len(lines[0]) - 1):
        for col_idx in range(1, len(lines) - 1):
            row = lines[row_idx]
            val = int(row[col_idx])
            # left
            left = 0
            for inner_col_idx in range(col_idx - 1, -1, -1):
                left_val = int(row[inner_col_idx])
                left += 1
                if left_val >= val:
                    break

            # right
            right = 0
            for col in range(col_idx + 1, cols):
                right_val = int(row[col])
                right += 1
                if right_val >= val:
                    break

            # top
            top = 0
            for top_idx in range(row_idx - 1, -1, -1):
                top_val = int(lines[top_idx][col_idx])
                top += 1
                if top_val >= val:
                    break

            # bottom
            bottom = 0
            for bottom_idx in range(row_idx + 1, rows):
                bottom_val = int(lines[bottom_idx][col_idx])
                bottom += 1
                if bottom_val >= val:
                    break

            non_zero = list(filter(lambda x: x != 0, [top, left, bottom, right]))
            if non_zero:
                non_zero_vals = reduce(lambda x, y: x*y, non_zero)
                scenic_score = max([scenic_score, non_zero_vals])

    return scenic_score


INPUT_S = """\
30373
25512
65332
33549
35390
"""
EXPECTED = 8


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
