#!/usr/bin/env python3

import os
import numpy as np
import re
import sys
from pprint import pprint

DEBUG = os.environ.get("DEBUG")

K = 14

def main():
    inp = open(sys.argv[1])

    for line in inp:
        line = line.rstrip()

        buffer = np.array(list(line))

        for i in range(len(buffer) - K):
            w = buffer[i:i+K]
            if np.unique(w).shape[0] == K:
                print(i + K)
                break

main()
