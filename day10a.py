#!/usr/bin/env python3

import io
import os
import numpy as np
import re
import sys
from pprint import pprint

DEBUG = os.environ.get("DEBUG")

def main():
    inp = open(sys.argv[1])

    t = 1
    cycle = []
    inc = []
    for line in inp:
        line = line.strip()
        if line == 'noop':
            t += 1
            continue

        t += 2
        w = line.split()
        k = int(w[1])
        cycle.append(t)
        inc.append(k)

    i_dx = np.transpose(np.array([cycle, inc], dtype=int))

    n = i_dx[-1, 0] + 1
    dx = np.zeros((n,), dtype=int)
    dx[i_dx[:, 0]] = i_dx[:, 1]
    dx[1] = 1

    x = np.cumsum(dx)

    i = np.array(range(20, 221, 40), dtype=int)
    sig = i * x[i]
    print(sig.sum())

main()
