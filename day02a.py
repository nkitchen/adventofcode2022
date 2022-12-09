#!/usr/bin/env python3

import os
import numpy as np
import sys

DEBUG = os.environ.get("DEBUG")

def main():
    inp = open(sys.argv[1]).read()

    # Translate X -> 1, Y -> 2, etc.
    tab = str.maketrans("ABCXYZ", "123123")
    numeric = inp.translate(tab)

    strategy = np.loadtxt(numeric.split('\n'), dtype=int)
    # strategy now has the form:
    #   opponent's move  my move
    #   1                2
    #   2                1
    #   3                3
    #
    # where 1=Rock, 2=Paper, 3=Scissors.

    his_play = strategy[:, 0]
    my_play = strategy[:, 1]
    d = (my_play - his_play) % 3
    win = (d == 1)
    draw = (d == 0)
    scores = my_play + 3 * draw + 6 * win
    print(scores.sum())

main()
