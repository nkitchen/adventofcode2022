#!/usr/bin/env python3

import io
import itertools
import os
import numpy as np
import re
import sys
from pprint import pprint

DEBUG = os.environ.get("DEBUG")
SHOW = os.environ.get("SHOW")

facing_chr = {
    (0, 1): '>',
    (0, -1): '<',
    (1, 0): 'V',
    (-1, 0): '^',
}

facing_num = {
    (0, 1): 0,
    (0, -1): 2,
    (1, 0): 1,
    (-1, 0): 3,
}

left_rotation = np.array([[0, -1], [1, 0]])

def main():
    inp = open(sys.argv[1]).read()

    map, path_descr = inp.split("\n\n")

    # Pad to same width.
    map_lines = map.split('\n')
    n = max(len(line) for line in map_lines)
    map_lines = [f"{line:{n}}" for line in map_lines]

    tiles = np.array([np.array(list(line)) for line in map_lines])
    trail = tiles.copy()

    def show():
        if not SHOW:
            return
        for row in trail:
            print(''.join(c for c in row))
        print()

    # Get to start position.
    facing = np.array([0, 1])
    pos = np.array([0, 0])
    while tiles[tuple(pos)] == ' ':
        pos += facing
    trail[tuple(pos)] = facing_chr[tuple(facing)]

    path_descr = path_descr.strip()
    i = 0
    path_re = re.compile(r"(\d+)|([RL])")
    while i < len(path_descr):
        m = path_re.match(path_descr, i)
        assert m
        i = m.end()

        if (d := m.group(1)):
            d = int(d)
            for j in range(d):
                npos = (pos + facing) % tiles.shape
                while tiles[tuple(npos)] == ' ':
                    npos = (npos + facing) % tiles.shape
                if tiles[tuple(npos)] == '.':
                    pos = npos
                    trail[tuple(pos)] = facing_chr[tuple(facing)]
                else:
                    assert tiles[tuple(npos)] == '#'
                    break
        elif (rot := m.group(2)) == 'L':
            facing = left_rotation @ facing
        else:
            assert rot == 'R'
            facing = -left_rotation @ facing

    show()

    password = 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + facing_num[tuple(facing)]
    print(password)

main()
