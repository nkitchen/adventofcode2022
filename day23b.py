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

    if SHOW:
        show(grove)

    dir_pref = ['north', 'south', 'west', 'east']

    for t in itertools.count(1):
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
        if DEBUG:
            breakpoint()

        nbrs = sum(grove[di:di+m-2, dj:dj+n-2]
                   for di in range(3)
                   for dj in range(3)
                   if (di, dj) != (1, 1))

        pending = grove[1:m-1, 1:n-1].copy()
        proposed = 0 * grove
        
        # Elves not moving
        nonmovers = pending * (nbrs == 0)
        if nonmovers.sum() == grove.sum():
            break
        proposed[1:m-1, 1:n-1] += nonmovers
        pending[nonmovers == 1] = 0

        # Elves proposing in each direction
        for dir in dir_pref:
            if dir == 'north':
                north_nbrs = sum(grove[0:m-2, dj:dj+n-2] for dj in range(3))
                north_proposers = pending * (north_nbrs == 0)
                proposed[0:m-2, 1:n-1] += north_proposers
                pending[north_proposers == 1] = 0
            elif dir == 'south':
                south_nbrs = sum(grove[2:m, dj:dj+n-2] for dj in range(3))
                south_proposers = pending * (south_nbrs == 0)
                proposed[2:m, 1:n-1] += south_proposers
                pending[south_proposers == 1] = 0
            elif dir == 'west':
                west_nbrs = sum(grove[di:di+m-2, 0:n-2] for di in range(3))
                west_proposers = pending * (west_nbrs == 0)
                proposed[1:m-1, 0:n-2] += west_proposers
                pending[west_proposers == 1] = 0
            elif dir == 'east':
                east_nbrs = sum(grove[di:di+m-2, 2:n] for di in range(3))
                east_proposers = pending * (east_nbrs == 0)
                proposed[1:m-1, 2:n] += east_proposers
                pending[east_proposers == 1] = 0

        # Elves who were blocked on all sides
        proposed[1:m-1, 1:n-1] += pending

        dest = proposed * (proposed < 2)

        north_aborters = north_proposers * (proposed[0:m-2, 1:n-1] > 1)
        dest[1:m-1, 1:n-1] += north_aborters
        south_aborters = south_proposers * (proposed[2:m, 1:n-1] > 1)
        dest[1:m-1, 1:n-1] += south_aborters
        west_aborters = west_proposers * (proposed[1:m-1, 0:n-2] > 1)
        dest[1:m-1, 1:n-1] += west_aborters
        east_aborters = east_proposers * (proposed[1:m-1, 2:n] > 1)
        dest[1:m-1, 1:n-1] += east_aborters

        grove = dest
        if SHOW:
            show(grove)

        dir_pref.append(dir_pref.pop(0))

    print(t)

def show(a):
    for row in a:
        s = ''.join(str(c) for c in row)
        s = s.replace('0', '.')
        s = s.replace('1', '#')
        print(s)
    print()

main()
