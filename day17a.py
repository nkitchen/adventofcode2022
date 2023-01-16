#!/usr/bin/env python3

import io
import itertools
import os
import numpy as np
import re
import sys
from pprint import pprint

DEBUG = os.environ.get("DEBUG")
SHOW = os.environ.get("SHOW")

def main():
    inp = open(sys.argv[1])
    jets = next(inp).strip()

    w = 7

    rock_shapes = """
0011110

0001000
0011100
0001000

0000100
0000100
0011100

0010000
0010000
0010000
0010000

0011000
0011000
"""
    rocks = [np.genfromtxt(io.StringIO(shape.strip()), dtype=int, delimiter=1)
             for shape in rock_shapes.split('\n\n')]
    for i in range(len(rocks)):
        if len(rocks[i].shape) == 1:
            rocks[i] = rocks[i][np.newaxis, :]

    rock_index = 0

    # Start with a floor.
    chamber = np.full((1, w), 1)

    rocks_dropped = 0

    def drop_rock():
        nonlocal chamber
        nonlocal rocks_dropped

        rock = rocks[rock_index]
        rocks_dropped += 1

        empty_rows = 0
        for row in chamber:
            if (row == 0).all():
                empty_rows += 1
            else:
                break

        gap = np.zeros((3, w), dtype=int)
        chamber = np.vstack((0 * rock, gap, chamber[empty_rows:, :]))

        return rock

    rock = drop_rock()
    h = rock.shape[0]
    fall = 0 # the distance fallen

    def show():
        ch = chamber.copy()
        ch[fall:fall + h, :] += 2 * rock
        print(ch)

    for jet in itertools.cycle(jets):
        if DEBUG:
            print(f"{jet=}")

        if jet == '<' and rock[:, 0].max() == 0:
            # Not at left edge
            pushed = np.roll(rock, -1, axis=1)
            if (chamber[fall:(fall + h), :] * pushed).max() == 0:
                # No collisions
                rock = pushed
        elif jet == '>' and rock[:, -1].max() == 0:
            # Not at right edge
            pushed = np.roll(rock, 1, axis=1)
            if (chamber[fall:(fall + h), :] * pushed).max() == 0:
                rock = pushed

        if (chamber[(fall + 1):(fall + h + 1), :] * rock).max() == 0:
            # No collisions below
            fall += 1
        else:
            chamber[fall:fall + h, :] += rock

            if rocks_dropped == 2022:
                # Subtract 1 for the floor.
                height = chamber.max(axis=1).sum() - 1
                print(height)
                return

            rock_index = (rock_index + 1) % len(rocks)
            rock = drop_rock()
            h = rock.shape[0]
            fall = 0 # the distance fallen

        if SHOW:
            show()
            breakpoint()

main()
