#!/usr/bin/env python3

import os
import numpy as np
import sys

DEBUG = os.environ.get("DEBUG")

def main():
    inp = open(sys.argv[1]).read()

    # Translate A -> 1 (Rock), B -> 2 (Paper), C -> 3 (Scissors)
    # and X -> 2 (== -1 mod 3), Y -> 0, Z -> 1.
    tab = str.maketrans("ABCXYZ", "123201")
    numeric = inp.translate(tab)

    strategy = np.loadtxt(numeric.split('\n'), dtype=int)
    # strategy now has the form:
    #   opponent's move  delta (my move - opponent's)
    #   1                0
    #   2                2
    #   3                1

    # Resulting in my moves:
    #   1
    #   1
    #   1

    his_play = strategy[:, 0]
    d = strategy[:, 1]
    # The offsets -1, +1 put the results in the range 1..3.
    my_play = (his_play + d - 1) % 3 + 1
    win = (d == 1)
    draw = (d == 0)
    scores = my_play + 3 * draw + 6 * win
    print(scores.sum())

main()
