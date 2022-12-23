#!/usr/bin/env python3

import io
import itertools
import os
import numpy as np
import re
import sys
from pprint import pprint

DEBUG = os.environ.get("DEBUG")

# This is about twice as fast as the much simpler obvious code, which is already too
# fast to matter.

def main():
    inp = open(sys.argv[1])
    heights = np.genfromtxt(inp, delimiter=1, dtype=int)

    m, n = heights.shape

    scenic = np.full((m, n), 1)

    for i in range(m):
        row = heights[(i,), :]
        northward = np.flip(heights[:i, :], axis=0)
        southward = heights[i+1:, :]
        nblocked = (northward >= row)
        sblocked = (southward >= row)

        if northward.shape[0] == 0:
            # No trees to the north
            nd = 0
        else:
            nk = np.argmax(nblocked, axis=0)
            # Case 1: The line has a blocking tree, so the argmax is the first index of
            #         blocked == True, and the number of visible trees is nk + 1.
            # Case 2: The line has no blocking tree, so the number of visible trees
            #         is the length of the line.
            nd = np.where(nblocked.any(axis=0), nk + 1, northward.shape[0])

        if southward.shape[0] == 0:
            # No trees to the south
            sd = 0
        else:
            sk = np.argmax(sblocked, axis=0)
            sd = np.where(sblocked.any(axis=0), sk + 1, southward.shape[0])

        scenic[i, :] *= nd * sd

    for j in range(n):
        col = heights[:, (j,)]
        westward = np.flip(heights[:, :j], axis=1)
        eastward = heights[:, j+1:]
        wblocked = (westward >= col)
        eblocked = (eastward >= col)

        if westward.shape[1] == 0:
            wd = 0
        else:
            wk = np.argmax(wblocked, axis=1)
            wd = np.where(wblocked.any(axis=1), wk + 1, westward.shape[1])

        if eastward.shape[1] == 0:
            ed = 0
        else:
            ek = np.argmax(eblocked, axis=1)
            ed = np.where(eblocked.any(axis=1), ek + 1, eastward.shape[1])

        scenic[:, j] *= wd * ed

    print(scenic.max())

import timeit
print(timeit.timeit(main, number=1))
#main()
