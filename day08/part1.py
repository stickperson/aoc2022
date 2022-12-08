from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> int:
    visible = 0
    lines = s.splitlines()
    rows = len(lines)
    cols = len(lines[0])
    for x in range(1, len(lines[0]) - 1):
        for y in range(1, len(lines) - 1):
            row = lines[x]
            val = int(row[y])

            # left
            is_visible = True
            for left_idx in range(0, y):
                left_val = int(row[left_idx])
                if val <= left_val:
                    is_visible = False
                    break

            if is_visible:
                visible += 1
                continue

            # right
            is_visible = True
            for right_idx in range(y + 1, cols):
                right_val = int(row[right_idx])
                if val <= right_val:
                    is_visible = False
                    break

            if is_visible:
                visible += 1
                continue

            # top
            is_visible = True
            for top_idx in range(0, x):
                top_val = int(lines[top_idx][y])
                if val <= top_val:
                    is_visible = False
                    break

            if is_visible:
                visible += 1
                continue

            # bottom
            is_visible = True
            for bottom_idx in range(x + 1, rows):
                bottom_val = int(lines[bottom_idx][y])
                if val <= bottom_val:
                    is_visible = False
                    break

            if is_visible:
                visible += 1
                continue

    border = len(lines) * 2
    inner = (len(lines[0]) - 2) * 2
    visible += border
    visible += inner
    return visible


INPUT_S = """\
30373
25512
65332
33549
35390
"""
EXPECTED = 21


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
