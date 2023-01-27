#!/usr/bin/env python3

import io
import os
import numpy as np
import re
import sys
from pprint import pprint
from collections import Counter

DEBUG = os.environ.get("DEBUG")

def main():
    inp = open(sys.argv[1])

    # shape=(n, 3)
    cubes = np.loadtxt(inp, delimiter=',')

    # Represent the sides of each cube as a point + or - 0.5 in each dimension.
    # shape=(1, 6, 3)
    dside = np.array([[[-0.5, 0,    0],
                       [+0.5, 0,    0],
                       [0,    -0.5, 0],
                       [0,    +0.5, 0],
                       [0,    0,    -0.5],
                       [0,    0,    +0.5]]])
    sides = cubes[:, np.newaxis, :] + dside
    n = sides.shape[0]
    sides = sides.reshape(n * 6, 3)

    count = Counter(tuple(sides[i])
                    for i in range(n * 6))
    area = sum(1 for s, k in count.items()
               if k == 1)
    print(area)

main()
