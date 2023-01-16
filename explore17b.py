#!/usr/bin/env python3

# Test script to explore the period of the repeating cycle

# Strategy: At some point the rock tower will have a repeating pattern with a cycle length
# that is a multiple of 5 * len(input).  But what multiple?  I don't know how many jets are
# used for each rock, so I can't say a priori.
#
# The first rocks won't necessarily stack in the repeating pattern.  To account
# for the time it takes to get into the pattern, and how the interactions with
# the walls may be different at first, I can include the chamber width into the
# number of initial drops before looking for the pattern:
#   5 * 7 * len(input).

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

    cycle_base = len(rocks) * len(jets)

    # The number of initial rocks dropped where I don't expect the cycle
    init_rocks = w * cycle_base

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

    cropped_height = 0

    def tower_height():
        assert chamber.max() == 1

        # Subtract 1 for the floor.
        return cropped_height + chamber.max(axis=1).sum() - 1

    prev_height = 0
    height_incrs = []

    cycle_multiple = 1

    def show():
        ch = chamber.copy()
        ch[fall:fall + h, :] += 2 * rock
        print(ch)

    for jet in itertools.cycle(jets):
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
            assert chamber.max() == 1

            # In initial experiments, I didn't see any rock fall more than 40 rows.
            # 50 seems like a safe number of rows to keep in the current window.
            m = chamber.shape[0]
            if m > 50:
                cropped_height += m - 50
                chamber = chamber[:50, :]

            height = tower_height()
            incr = height - prev_height
            prev_height = height

            if rocks_dropped > init_rocks:
                height_incrs.append(incr)

            cycle = cycle_base * cycle_multiple
            if len(height_incrs) == len(jets) * cycle:
                a = np.array(height_incrs).reshape((len(jets), cycle))
                if (a[0, :] == a[1:, :]).all():
                    print(f"{cycle_multiple=}")
                    return

                cycle_multiple += 1

            rock_index = (rock_index + 1) % len(rocks)
            rock = drop_rock()
            h = rock.shape[0]
            fall = 0 # the distance fallen

        if SHOW:
            show()
            breakpoint()

main()
