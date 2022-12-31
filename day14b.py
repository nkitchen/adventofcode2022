#!/usr/bin/env python3

import io
import os
import numpy as np
import re
import sys
from pprint import pprint

DEBUG = os.environ.get("DEBUG")
SHOW = os.environ.get("SHOW")

def parse_pair(s):
    w = s.split(',')
    x = int(w[0])
    y = int(w[1])
    return np.array([x, y])

AIR = '.'
ROCK = '#'
SAND = 'o'

def main():
    inp = open(sys.argv[1])

    paths = []
    for line in inp:
        path = np.vstack(tuple(parse_pair(p) for p in re.findall(r"(\d+,\d+)", line)))
        paths.append(path)

    y_min = 0
    y_max = 2 + max(path[:, 1].max() for path in paths)
    x_min = min(500 - y_max - 1, *(path[:, 0].min() for path in paths))
    x_max = max(500 + y_max + 1, *(path[:, 0].max() for path in paths))
    a = x_min - 1
    b = 0

    offset = np.array([a, b])
    cave = np.full((x_max - x_min + 2, y_max - y_min + 2), AIR, dtype='<U1')

    cave[500 - a, 0 - b] = '+'
    cave[:, y_max - b] = ROCK

    for path in paths:
        for i in range(len(path) - 1):
            v = path[i + 1] - path[i]
            d = abs(v).max()
            for p in np.linspace(path[i], path[i + 1], d + 1, dtype=int):
                cave[tuple(p - offset)] = ROCK

    def show():
        for y in range(cave.shape[1]):
            print(''.join(cave[:, y]))
        print()

    if SHOW:
        show()

    while True:
        x, y = 500, 0
        while x_min <= x <= x_max and y_min <= y <= y_max:
            at_rest = True
            for xn, yn in [
                (x, y + 1),
                (x - 1, y + 1),
                (x + 1, y + 1),
            ]:
                if cave[xn - a, yn - b] == AIR:
                    x, y = xn, yn
                    at_rest = False
                    break

            if at_rest:
                cave[x - a, y - b] = SAND
                break

        if SHOW:
            show()

        if x == 500 and y == 0:
            break

    show()
    print((cave == SAND).sum())

main()
