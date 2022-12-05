from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(s: str) -> str:
    stacks = []
    crates, instructions = s.split("\n\n")
    crates = crates.splitlines()[:-1]
    for idx in range(0, len(crates[0]), 4):
        stacks.append([])
    for crate_row in crates:
        for idx in range(0, len(crate_row), 4):
            stack_number = idx // 4
            crate = crate_row[idx:idx + 4]
            crate = crate.strip()
            if crate:
                stacks[stack_number].append(crate)
    temp_stacks = []
    for stack in stacks:
        temp_stacks.append(stack[::-1])
    stacks = temp_stacks

    for instruction in instructions.splitlines():
        parts = instruction.split()
        amount = int(parts[1])
        from_stack = int(parts[3]) - 1
        to_stack = int(parts[-1]) - 1
        to_add = []
        while amount:
            to_add.append(stacks[from_stack].pop())
            amount -= 1
        while to_add:
            stacks[to_stack].append(to_add.pop())
    ans = []
    for stack in stacks:
        crate = stack[-1][1]
        ans.append(crate)
    ans = "".join(ans)
    return ans


INPUT_S = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""
EXPECTED = "MCD"


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
