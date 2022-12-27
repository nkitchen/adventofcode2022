#!/usr/bin/env python3

import io
import os
import numpy as np
import re
import sys
import time
from pprint import pprint

DEBUG = os.environ.get("DEBUG")
DISPLAY = os.environ.get("DISPLAY")

def main():
    inp = open(sys.argv[1])
    heightmap = np.genfromtxt(inp, delimiter=1, dtype='<U1')

    start = np.hstack((heightmap == 'S').nonzero())
    goal = np.hstack((heightmap == 'E').nonzero())
    heightmap[heightmap == 'S'] = 'a'
    heightmap[heightmap == 'E'] = 'z'

    elev = np.array([ord(c) for c in heightmap.flatten()]).reshape(heightmap.shape) - ord('a')

    m, n = elev.shape
    delta = np.array([[-1, 0],
                      [+1, 0],
                      [0, -1],
                      [0, +1]])

    def neighbors(pos):
        for d in delta:
            npos = pos + d
            if 0 <= npos[0] < m and 0 <= npos[1] < n:
                yield npos

    pos = np.hstack(start)
    steps = np.full((m, n), -1)
    q = [pos]
    while q:
        pos = q[0]
        q = q[1:]

        tpos = tuple(pos)
        for npos in neighbors(pos):
            tnpos = tuple(npos)
            if elev[tnpos] <= elev[tpos] + 1:
                if steps[tnpos] < 0:
                    steps[tnpos] = 1 + steps[tpos]
                    if (npos == goal).all():
                        return steps[tnpos]

                    q.append(npos)

            if DISPLAY:
                try:
                    os.ttyname(1)
                    os.system("clear")
                except OSError:
                    pass

                h = heightmap.copy()
                h[steps >= 0] = '#'
                np.savetxt(sys.stdout, h, fmt='%s')
                time.sleep(0.01)

r = main()
print(r)
