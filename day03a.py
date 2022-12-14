#!/usr/bin/env python3

import os
import numpy as np
import sys

DEBUG = os.environ.get("DEBUG")

def main():
    priority_sum = 0

    inp = open(sys.argv[1])
    for line in inp:
        rucksack = np.array(list(line.strip()))
        n = len(rucksack)
        c1 = rucksack[:n//2]
        c2 = rucksack[n//2:]
        items = np.intersect1d(c1, c2)
        assert len(items) == 1

        x = items[0]
        if 'a' <= x <= 'z':
            priority = ord(x) - ord('a') + 1
        elif 'A' <= x <= 'Z':
            priority = ord(x) - ord('A') + 27
        else:
            assert False

        priority_sum += priority

    print(priority_sum)

main()
