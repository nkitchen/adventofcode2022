#!/usr/bin/env python3

import os
import numpy as np
import sys

DEBUG = os.environ.get("DEBUG")

def main():
    inp = open(sys.argv[1])
    rucksacks = [np.array(list(line.strip()))
                 for line in inp]

    priority_sum = 0
    for g in range(0, len(rucksacks), 3):
        r1, r2, r3 = rucksacks[g:g+3]
        badge = np.intersect1d(r1, r2)
        badge = np.intersect1d(badge, r3)

        assert len(badge) == 1

        x = badge[0]
        if 'a' <= x <= 'z':
            priority = ord(x) - ord('a') + 1
        elif 'A' <= x <= 'Z':
            priority = ord(x) - ord('A') + 27
        else:
            assert False

        priority_sum += priority

    print(priority_sum)

main()
