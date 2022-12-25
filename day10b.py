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

    n = max(i_dx[-1, 0] + 1, 241)
    dx = np.zeros((n,), dtype=int)
    dx[i_dx[:, 0]] = i_dx[:, 1]
    dx[1] = 1

    x = np.cumsum(dx)

    crt = []
    for t in range(1, 241):
        i = (t - 1) % 40
        v = x[t]
        if v - 1 <= i <= v + 1:
            crt.append('#')
        else:
            crt.append('.')
        if t % 40 == 0:
            crt.append('\n')
    print(''.join(crt))

main()
