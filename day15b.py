#!/usr/bin/env python3

import io
import os
import numpy as np
import re
import sys
import time
from pprint import pprint
from collections import defaultdict

DEBUG = os.environ.get("DEBUG")
SHOW = os.environ.get("SHOW")

def l1dist(p, q):
    return abs(p - q).sum(axis=1)

def main():
    inp = open(sys.argv[1]).read()

    tab = (inp.replace('Sensor at x=', '')
           .replace(', y=', ' ')
           .replace(': closest beacon is at x=', ' '))
    data = np.genfromtxt(io.StringIO(tab), dtype=int)

    xy_min = 0
    if len(sys.argv) > 2:
        xy_max = int(sys.argv[2])
    else:
        xy_max = 4000000

    sensor = data[:, 0:2]
    beacon = data[:, 2:4]

    # Every sensor defines a coverage area:
    #    |x - sx| + |y - sy| <= d
    mindist = l1dist(sensor, beacon)

    # or:
    #    -d <= x - sx + y - sy <= d
    #    -d <= x - sx - y + sy <= d

    # Change of variables: u = x + y, v = x - y
    #    -d <= u - sx - sy <= d
    #    -d <= v - sx + sy <= d
    # or:
    #    -d + sx + sy <= u <= d + sx + sy
    #    -d + sx - sy <= v <= d + sx - sy
    u_lower = sensor[:, 0] + sensor[:, 1] - mindist
    u_upper = sensor[:, 0] + sensor[:, 1] + mindist
    v_lower = sensor[:, 0] - sensor[:, 1] - mindist
    v_upper = sensor[:, 0] - sensor[:, 1] + mindist

    # For a given u, we can find the union of covered v intervals.
    # The coverage only changes at the u bounds, so we need only check the
    # intervals around those values.
    u_check = np.stack((u_lower - 1, u_lower, u_lower + 1,
                        u_upper - 1, u_upper, u_upper + 1))
    for u in np.nditer(u_check):
        # Which other sensor areas overlap with this u value?
        u_overlap = (u_lower <= u) & (u <= u_upper)
        spans = []
        for i, ov in enumerate(u_overlap):
            if ov:
                spans.append([v_lower[i], v_upper[i]])

        spans.sort()
        if not spans:
            continue

        combined_spans = [spans[0]]
        for span in spans[1:]:
            last_span = combined_spans[-1]
            if last_span[1] + 1 >= span[0]:
                # Adjacent/overlapping
                last_span[1] = max(last_span[1], span[1])
            else:
                combined_spans.append(span)

        if len(combined_spans) > 1:
            v = combined_spans[0][1] + 1
            x = (u + v) // 2
            y = u - x
            if x in range(0, xy_max) and y in range(0, xy_max):
                print(x, y)

    freq = x * 4000000 + y
    print(freq)

main()

# Combinatorics: We can afford quadratic scaling, but not exponential (n=36).
