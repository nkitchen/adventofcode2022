#!/usr/bin/env python3

import io
import os
import numpy as np
import re
import sys
from pprint import pprint
from collections import defaultdict

DEBUG = os.environ.get("DEBUG")

def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

def main():
    inp = open(sys.argv[1])

    a_lava = np.loadtxt(inp, delimiter=',', dtype=int)

    s_lava = set(tuple(v) for v in a_lava)

    OUTSIDE = 0
    LAVA = 1
    BETWEEN = 2

    c_class = defaultdict(int)
    for c in s_lava:
        c_class[c] = LAVA

    # Find cubes that are Between cubes of Lava.

    lava_by_xy = defaultdict(list)
    for cube in s_lava:
        lava_by_xy[cube[:2]].append(cube)

    for a in lava_by_xy.values():
        a.sort()

    for xy, line in lava_by_xy.items():
        for z in range(line[0][2], line[-1][2] + 1):
            c = xy + (z,)
            if c not in s_lava:
                c_class[c] = BETWEEN

    def _neighbors(c):
        for i in range(len(c)):
            a = list(c)
            a[i] -= 1
            yield tuple(a)
            a[i] += 2
            yield tuple(a)

    # For each Between cube:
    #   If it has a neighbor that is Outside,
    #     Change its class to Outside, and put it on the queue.
    queue = []
    for cube, cl in c_class.items():
        if cl != BETWEEN:
            continue
        if any(c_class.get(n, OUTSIDE) == OUTSIDE for n in _neighbors(cube)):
            c_class[cube] = OUTSIDE
            queue.append(cube)

    # Propagate the Outside class as long as we keep finding neighboring Between cubes.
    while queue:
        c = queue[0]
        queue = queue[1:]

        for n in _neighbors(c):
            if c_class[n] == BETWEEN:
                c_class[n] = OUTSIDE
                queue.append(n)

    if len(sys.argv) > 2:
        with open(sys.argv[2], "w") as f:
            for cube, cl in c_class.items():
                print(f"{cube[0]} {cube[1]} {cube[2]} {cl}", file=f)

    # For each Lava cube:
    #   Count the neighbors that are Outside.
    area = 0
    for c in s_lava:
        for n in _neighbors(c):
            dprint(f"{c} neighbor: {n} {c_class[n]}")
            if c_class[n] == OUTSIDE:
                area += 1
    print(area)

main()
