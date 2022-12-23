#!/usr/bin/env python3

import io
import os
import numpy as np
import re
import sys
from pprint import pprint

DEBUG = os.environ.get("DEBUG")

def vec(*x):
    return np.array(x, dtype=int)

def main():
    N = 10
    knots = np.zeros((N, 2))
    
    dirVec = {
        'L': vec(0, -1),
        'R': vec(0, +1),
        'U': vec(-1, 0),
        'D': vec(+1, 0),
    }

    tail = knots[-1]
    visited = set([tuple(tail)])

    inp = open(sys.argv[1])
    for line in inp:
        dir, dist = line.split()
        dist = int(dist)
        if DEBUG:
            print(f"{dir=} {dist=}")

        for k in range(dist):
            # Move the head.
            knots[0] += dirVec[dir]

            for i in range(N - 1):
                d = knots[i] - knots[i + 1]
                if DEBUG:
                    print(f"d={d}")
                if abs(d).max() <= 1:
                    # Following knot is still adjacent.
                    continue

                # >>> Add d, but limited to 1 in each dimension.
                e = np.clip(d, -1, 1)
                knots[i + 1] += e

            tail = knots[-1]
            visited.add(tuple(tail))

    print(len(visited))

main()
