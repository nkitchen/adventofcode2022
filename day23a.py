#!/usr/bin/env python3

import io
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

    elf_ij = np.argwhere(grove) # shape (nelf, 2)

    # Pad to ensure empty margin.
    empty_row = np.zeros((1, grove.shape[1]), dtype=int)
    if (elf_ij[:, 0] == 0).any():
        grove = np.vstack((empty_row, grove))
        elf_ij += (1, 0)
    if (elf_ij[:, 0] == grove.shape[0] - 1).any():
        grove = np.vstack((grove, empty_row))
    empty_col = np.zeros((grove.shape[0], 1), dtype=int)
    if (elf_ij[:, 1] == 0).any():
        grove = np.hstack((empty_col, grove))
        elf_ij += (0, 1)
    if (elf_ij[:, 1] == grove.shape[1] - 1).any():
        grove = np.hstack((grove, empty_col))

    nbr_ij = elf_ij[:, np.newaxis, :] + nbr_offsets[np.newaxis, ...]
    # >>> shape (nelf, nnbr, 2)

    print(at(grove, nbr_ij).any(axis=1))

def at(map, idxs):
    return map[(idxs[..., 0], idxs[..., 1])]

main()
