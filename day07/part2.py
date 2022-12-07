from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


class Directory:
    def __init__(self, name: str, parent=None):
        self.name = name
        self.parent = parent
        self.files = []
        self.subdirectories = {}
        self._size = 0

    @property
    def size(self):
        if self._size:
            return self._size
        _size = sum(self.files)
        for subdir in self.subdirectories.values():
            _size += subdir.size
        self._size = _size
        return self._size


def compute(s: str) -> int:
    root = Directory("/")
    current_dir = root
    for line in s.splitlines()[1:]:
        line_parts = line.split()
        if line_parts[0] == "$":
            if line_parts[1] == "cd":
                cd_dir = line_parts[2]
                if cd_dir == "/":
                    while current_dir.parent:
                        current_dir = current_dir.parent
                elif cd_dir == "..":
                    current_dir = current_dir.parent
                else:
                    current_dir = current_dir.subdirectories[cd_dir]

        elif line_parts[0] == "dir":
            dirname = line_parts[1]
            directory = Directory(dirname, parent=current_dir)
            current_dir.subdirectories[dirname] = directory
        else:
            current_dir.files.append(int(line_parts[0]))
    sizes = []
    subdirectories = list(root.subdirectories.values())
    available = 70000000 - root.size
    required = 30000000 - available
    while subdirectories:
        current = subdirectories.pop()
        if current.size >= required:
            sizes.append(current.size)
        subdirectories.extend(current.subdirectories.values())

    return min(sizes)


INPUT_S = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
EXPECTED = 24933642


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
