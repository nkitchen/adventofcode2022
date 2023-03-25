#!/usr/bin/env python3

import io
import itertools
import os
import numpy as np
import re
import sys
import time
from pprint import pprint

DEBUG = os.environ.get("DEBUG")
SHOW = os.environ.get("SHOW")

nbr_offsets = np.array([[-1, -1], [-1, 0], [-1, 1],
                        [ 0, -1],          [ 0, 1],
                        [ 1, -1], [ 1, 0], [ 1, 1]], dtype=int)

def main():
    inp = open(sys.argv[1]).read()
    inp = inp.replace('.', '0')
    inp = inp.replace('#', '1')
    grove = np.genfromtxt(inp.split('\n'), delimiter=1, dtype=int)

    # Pad to ensure empty margin.
    empty_row = np.zeros((1, grove.shape[1]), dtype=int)
    if grove[0, :].any():
        grove = np.vstack((empty_row, grove))
    if grove[-1, :].any():
        grove = np.vstack((grove, empty_row))
    empty_col = np.zeros((grove.shape[0], 1), dtype=int)
    if grove[:, 0].any():
        grove = np.hstack((empty_col, grove))
    if grove[:, -1].any():
        grove = np.hstack((grove, empty_col))

    m, n = grove.shape

    nbrs = sum(grove[di:di+m-2, dj:dj+n-2]
               for di in range(3)
               for dj in range(3)
               if (di, dj) != (1, 1))

    pending = grove[1:m-1, 1:n-1]
    proposed = 0 * grove
    
    # Elves not moving
    proposed[1:m-1, 1:n-1] += pending * (nbrs == 0)
    pending *= (nbrs != 0)

    # Elves proposing in each direction
    north_nbrs = sum(grove[0:m-2, dj:dj+n-2] for dj in range(3))
    proposed[0:m-2, 1:n-1] += pending * (north_nbrs == 0)
    pending *= (north_nbrs != 0)

    south_nbrs = sum(grove[2:m, dj:dj+n-2] for dj in range(3))
    proposed[2:m, 1:n-1] += pending * (south_nbrs == 0)
    pending *= (south_nbrs != 0)

    west_nbrs = sum(grove[di:di+m-2, 0:n-2] for di in range(3))
    proposed[1:m-1, 0:n-2] += pending * (west_nbrs == 0)
    pending *= (west_nbrs != 0)

    east_nbrs = sum(grove[di:di+m-2, 2:n] for di in range(3))
    proposed[1:m-1, 2:n] += pending * (east_nbrs == 0)
    pending *= (east_nbrs != 0)

    # Now we can easily tell where there are collisions, but how do
    # we tell which elves to keep in place?

main()
