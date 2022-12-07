#!/usr/bin/env python3

import os
import numpy as np
import sys

DEBUG = os.environ.get("DEBUG")

def main():
    inp = open(sys.argv[1]).read()
    inventory_per_elf = inp.split('\n\n')
    calories = [np.fromstring(inv, dtype=int, sep='\n')
                for inv in inventory_per_elf]

    n = max(len(c) for c in calories)
    for i, _ in enumerate(calories):
        calories[i].resize(n, refcheck=False)

    calories = np.array(calories)

    carried = calories.sum(axis=1)
    print(carried.max())

main()
