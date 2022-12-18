#!/usr/bin/env python3

import os
import numpy as np
import re
import sys
from pprint import pprint

DEBUG = os.environ.get("DEBUG")

K = 4

def main():
    inp = open(sys.argv[1])

    for line in inp:
        line = line.rstrip()

        buffer = np.array(list(line))

        for i in range(len(buffer) - K):
            w = buffer[i:i+4]
            if np.unique(w).shape == (K,):
                print(i + K)
                break

main()
