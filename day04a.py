#!/usr/bin/env python3

import os
import numpy as np
import sys

DEBUG = os.environ.get("DEBUG")

def main():
    inp = open(sys.argv[1]).read()
    # 2-4,6-8
    # 2-3,4-5

    wsep = inp.replace("-", " ").replace(",", " ")
    # 2 4 6 8
    # 2 3 4 5

    assignments = np.loadtxt(wsep.split('\n'), dtype=int)
    p = assignments[:, 0:2]
    q = assignments[:, 2:4]

    a = np.maximum(p[:,0], q[:,0])
    b = np.minimum(p[:,1], q[:,1])
    overlap = np.stack((a, b), axis=-1)

    contained = ((overlap == p).all(1) |
                 (overlap == q).all(1))
    print(contained.sum())

main()
