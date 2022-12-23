#!/usr/bin/env python3

import io
import itertools
import os
import numpy as np
import re
import sys
from pprint import pprint

DEBUG = os.environ.get("DEBUG")

def main():
    inp = open(sys.argv[1])
    heights = np.genfromtxt(inp, delimiter=1, dtype=int)

    m, n = heights.shape

    scenic = np.full((m, n), 1)

    for i, j in itertools.product(range(m), range(n)):
        h = heights[i, j]
        nd = 0
        for ii in range(i - 1, -1, -1):
            nd += 1
            if heights[ii, j] >= h:
                break
        sd = 0
        for ii in range(i + 1, m):
            sd += 1
            if heights[ii, j] >= h:
                break
        wd = 0
        for jj in range(j - 1, -1, -1):
            wd += 1
            if heights[i, jj] >= h:
                break
        ed = 0
        for jj in range(j + 1, n):
            ed += 1
            if heights[i, jj] >= h:
                break
        scenic[i, j] = nd * sd * wd * ed


    print(scenic.max())

import timeit
print(timeit.timeit(main, number=1))
#main()
