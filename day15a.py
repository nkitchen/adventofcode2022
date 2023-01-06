#!/usr/bin/env python3

import io
import os
import numpy as np
import re
import sys
import time
from pprint import pprint

DEBUG = os.environ.get("DEBUG")
DISPLAY = os.environ.get("DISPLAY")

def main():
    inp = open(sys.argv[1]).read()

    tab = (inp.replace('Sensor at x=', '')
           .replace(', y=', ' ')
           .replace(': closest beacon is at x=', ' '))
    data = np.genfromtxt(io.StringIO(tab), dtype=int)

    sensor = data[:, 0:2]
    beacon = data[:, 2:4]
    mindist = abs(sensor - beacon).sum(axis=1)

    if len(sys.argv) > 2:
        target_row = int(sys.argv[2])
    else:
        target_row = 2000000

    dy = abs(sensor[:, 1] - target_row)
    dx = mindist - dy

    target_spans = []
    for i in range(len(sensor)):
        if dy[i] > mindist[i]:
            continue

        x = sensor[i][0]
        target_spans.append([x - dx[i], x + dx[i]])

    target_spans.sort()

    combined_spans = [target_spans[0]]
    for span in target_spans[1:]:
        last_span = combined_spans[-1]
        if span[0] <= last_span[1]:
            # Overlap
            last_span[1] = max(last_span[1], span[1])
        else:
            combined_spans.append(span)

    covered = 0
    for span in combined_spans:
        covered += span[1] - span[0] + 1

    # Remove beacons in the row.
    for b in np.unique(beacon, axis=0):
        if b[1] == target_row:
            covered -= 1

    print(covered)

main()

"""
               1    1    2    2
     0    5    0    5    0    5
-2 ....h.....g.................
-1 ...hhh...ggg................
 0 ..hhShh.ggggg...............
 1 ...hhh.ggggggg........S.....
 2 ....h.gggggggggS............
 3 ....hgggggggggggSB..........
 4 ....hgggggggggggg...........
 5 ...ghggggggggggggg..........
 6 ..gghgggggggggggggg.........
 7 .ggghgggggSgggggggSg........
 8 ..gghgggggggggggggg.........
 9 ..ighgggggggggggggl.........
10 iiiiBgggggggggdggljjjjjjjjj.
11 .iSiaggggggggddd......j.....
12 .iiaaaggggggddddd.....j.....
13 ..aaaaaggggddddddd....j.....
14 .aaaaaaaggddddSdddd...S.....
15 Baaaaaaaaggddddddd..........
16 aaaaaaaaaagSBdddd...........
17 aaaaaaaaaaa..dddS..........B
18 aaaaSaaaaaaa..d.............
19 aaaaaaaaaaa.................
20 aaaaaaaaaa..S......S........
21 aaaaaaaaa...................
22 .aaaaaaa...............B....
23 ..aaaaa.....................
24 ...aaa......................

                           1         1         2         2 
       0         5         0         5         0         5 
-2 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
-1 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
 0 . . . . S . . . . . . . . . . . . . . . . . . . . . . . 
 1 . . . . . . . . . . . . . . . . . . . . . . S . . . . . 
 2 . . . . . . . . . . . . . . . S . . . . . . . . . . . . 
 3 . . . . . . . . . . . . . . . . S B . . . . . . . . . . 
 4 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
 5 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
 6 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
 7 . . . . . . . . . . S . . . . . . . S . . . . . . . . . 
 8 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
 9 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
10 . . . . B . . . . . . . . . . . . . . . . . . . . . . . 
11 . . S . . . . . . . . . . . . . * . . . . . . . . . . . 
12 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
13 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
14 . . . . . . . . . . . . . . S . . . . . . . S . . . . . 
15 B . . . . . . . . . . . . . . . . . . . . . . . . . . . 
16 . . . . . . . . . . . S B . . . . . . . . . . . . . . . 
17 . . . . . . . . . . . . . . . . S . . . . . . . . . . B 
18 . . . . S . . . . . . . . . . . . . . . . . . . . . . . 
19 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
20 . . . . . . . . . . . . S . . . . . . S . . . . . . . . 
21 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
22 . . . . . . . . . . . . . . . . . . . . . . . B . . . . 
23 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
24 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
"""
