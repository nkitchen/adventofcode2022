#!/usr/bin/env python3

import heapq
import os
import numpy as np
import re
import sys
from pprint import pprint
from collections import namedtuple

DEBUG = os.environ.get("DEBUG")
SHOW = os.environ.get("SHOW")

def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

class State(namedtuple('State', 'i j elapsed')):
    pass

def main():
    inp = open(sys.argv[1])
    map = np.genfromtxt(inp, delimiter=1, dtype='<U1', comments=None)

    m, n = map.shape

    # Blizzards heading each direction
    blizzards = {
        'w': map[1:m-1, 1:n-1] == '<',
        'e': map[1:m-1, 1:n-1] == '>',
        'n': map[1:m-1, 1:n-1] == '^',
        's': map[1:m-1, 1:n-1] == 'v',
    }

    start = State(0, 1, 0)
    final = search(map, start, blizzards)
    print(final.elapsed)

def search(map, start, blizzards):
    """A* search"""

    m, n = map.shape
    assert map[0, 1] == '.'
    assert map[m-1, n-2] == '.'

    goal = (m-1, n-2)

    visited = set(start)
    queue = [(estimate_from(start, goal), start)]
    while queue:
        h, s = heapq.heappop(queue)
        dprint(f"popped {s}")
        if (s.i, s.j) == goal:
            return s

        for t in neighbor_states(s, map, blizzards):
            if t in visited:
                continue
            dprint(f"  neighbor {t} pushed")

            visited.add(t)
            h = t.elapsed + estimate_from(t, goal)
            heapq.heappush(queue, (h, t))

    return None

def neighbor_states(s, map, blizzards):
    m, n = map.shape
    candidates = []
    if s.i > 0:
        candidates.append(State(s.i - 1, s.j, s.elapsed + 1))
    if s.j > 0:
        candidates.append(State(s.i, s.j - 1, s.elapsed + 1))
    if s.i < m - 1:
        candidates.append(State(s.i + 1, s.j, s.elapsed + 1))
    if s.j < n - 1:
        candidates.append(State(s.i, s.j + 1, s.elapsed + 1))
    candidates.append(State(s.i, s.j, s.elapsed + 1))

    mm = m - 2
    nn = n - 2
    for c in candidates:
        if map[c.i, c.j] == '#':
            continue

        if c.i in (0, m - 1):
            # No blizzards
            yield c
            continue
        if c.j in (0, n - 1):
            yield c
            continue

        # The position of blizzards is uniquely determined by the time.
        # There is a southward-moving blizzard at i, j at time t ==>
        #   There was a blizzard at (u = i - t), v at time 0.
        # (Subtract 1 for north and west borders.)
        if blizzards['n'][(c.i - 1 + c.elapsed) % mm, c.j - 1]:
            continue
        if blizzards['s'][(c.i - 1 - c.elapsed) % mm, c.j - 1]:
            continue
        if blizzards['w'][c.i - 1, (c.j - 1 + c.elapsed) % nn]:
            continue
        if blizzards['e'][c.i - 1, (c.j - 1 - c.elapsed) % nn]:
            continue

        yield c

def estimate_from(s, goal):
    return abs(s.i - goal[0]) + abs(s.j - goal[1])

main()
