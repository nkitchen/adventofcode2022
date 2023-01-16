#!/usr/bin/env python3

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
import signal
import sys
from pprint import pprint

DEBUG = os.environ.get("DEBUG")
SHOW = os.environ.get("SHOW")

ROCKS_TO_DROP = 1000000000000

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

    # The number of rocks dropped before I expect the cycle
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
    cycle_rocks = None

    def show():
        ch = chamber.copy()
        ch[fall:fall + h, :] += 2 * rock
        print(ch)

    def sig_status(signum, frame):
        print(f"rocks_dropped={rocks_dropped}")
        print(f"cycle_multiple={cycle_multiple}")
        sys.stdout.flush()
    signal.signal(signal.SIGUSR1, sig_status)

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

            if rocks_dropped == init_rocks:
                prev_height = init_height = tower_height()

            if rocks_dropped > init_rocks:
                if cycle_rocks is None:
                    height = tower_height()
                    incr = height - prev_height
                    height_incrs.append(incr)
                    prev_height = height

                    cyc = cycle_base * cycle_multiple
                    k = 3
                    if len(height_incrs) == k * cyc:
                        if all(height_incrs[:cyc] == height_incrs[i*cyc:(i+1)*cyc]
                               for i in range(1, k)):
                            cycle_rocks = cyc
                            cycle_height = sum(height_incrs[:cyc])
                            coda_rocks = (ROCKS_TO_DROP - init_rocks) % cycle_rocks
                        else:
                            cycle_multiple += 1
                elif (rocks_dropped - init_rocks) % cycle_rocks == coda_rocks:
                    coda_height = tower_height() - prev_height
                    break

            rock_index = (rock_index + 1) % len(rocks)
            rock = drop_rock()
            h = rock.shape[0]
            fall = 0 # the distance fallen

        if SHOW:
            show()
            breakpoint()

    print(f"cycle_multiple={cycle_multiple}")
    print(f"cycle_height={cycle_height}")
    cycles = (ROCKS_TO_DROP - init_rocks - coda_rocks) // cycle_rocks
    n = init_height + cycles * cycle_height + coda_height
    print(n)

main()

# Runtime: 167m30.790s !!
# cycle_multiple=341
