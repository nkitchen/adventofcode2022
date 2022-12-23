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
    start = vec(0, 0)
    # Avoid aliasing.
    head = start.copy()
    tail = start.copy()
    
    dirVec = {
        'L': vec(0, -1),
        'R': vec(0, +1),
        'U': vec(-1, 0),
        'D': vec(+1, 0),
    }

    visited = set([tuple(start)])

    inp = open(sys.argv[1])
    for line in inp:
        dir, dist = line.split()
        dist = int(dist)
        if DEBUG:
            print(f"{dir=} {dist=}")

        for i in range(dist):
            head += dirVec[dir]

            d = head - tail
            if DEBUG:
                print(f"d={d}")
            if abs(d).max() <= 1:
                # Tail is still adjacent.
                continue

            # Case: d = (+2, 0)  >>> tail += (+1, 0)
            # Case: d = (-2, 0)  >>> tail += (-1, 0)
            # Case: d = (0, +2)  >>> tail += (0, +1)
            # Case: d = (0, -2)  >>> tail += (0, -1)
            # Case: d = (+2, +1) >>> tail += (+1, +1)
            # Case: d = (+2, -1) >>> tail += (+1, -1)
            # Etc.
            
            # >>> Add d, but limited to 1 in each dimension.
            e = np.clip(d, -1, 1)
            tail += e

            visited.add(tuple(tail))

    print(len(visited))

main()
