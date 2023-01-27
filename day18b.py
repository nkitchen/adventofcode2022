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

    # Looking at the point cloud, it appears that the lava droplet is concave, and so
    # it's easy to recognize air pockets by simply comparing to the min and max lava cubes 
    # in a line through the droplet.

    # An approach for the general case is at the bottom of this file.

    s_lava = set(tuple(v) for v in a_lava)

    lava_by_xy = defaultdict(list)
    for cube in s_lava:
        lava_by_xy[cube[:2]].append(cube)

    for a in lava_by_xy.values():
        a.sort()

    def is_outside(c):
        s = lava_by_xy.get(c[:2], None)
        return not s or c[2] < s[0][2] or c[2] > s[-1][2]

    def _neighbors(c):
        for i in range(len(c)):
            a = list(c)
            a[i] -= 1
            yield tuple(a)
            a[i] += 2
            yield tuple(a)

    area = 0
    for c in s_lava:
        for n in _neighbors(c):
            dprint(f"{c} neighbor: {n} ", end='')
            if n in s_lava:
                dprint("lava")
            elif is_outside(n):
                dprint("outside")
                area += 1
            else:
                dprint("inside")
    print(area)

main()

# If the lava droplet were not convex, this would be my approach:
#
#   Find cubes that are Between cubes of Lava.
#   Put all Between cubes on queue.
#   For each cube on queue:
#       If it has a neighbor that is Outside,
#       Change its class to Outside and put its Between neighbors on the queue.
#
#   For each Lava cube:
#       Count the neighbors that are Outside.
