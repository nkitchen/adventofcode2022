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
    heights = np.genfromtxt(inp, delimiter=1, dtype=int)

    m, n = heights.shape
    visible = np.full((m, n), False)

    for i in range(0, m):
        row = heights[(i,), :]
        north = heights[:i, :]
        south = heights[i+1:, :]
        vn = (row > north).all(axis=0)
        vs = (row > south).all(axis=0)
        visible[i, :] |= vn
        visible[i, :] |= vs

    for j in range(0, n):
        col = heights[:, (j,)]
        west = heights[:, :j]
        east = heights[:, j+1:]
        vw = (col > west).all(axis=1)
        ve = (col > east).all(axis=1)
        visible[:, j] |= vw
        visible[:, j] |= ve

    print(visible.sum())

main()
