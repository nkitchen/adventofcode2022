#!/usr/bin/env python3

import functools
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

class State(namedtuple('State', 'pos goals elapsed')):
    @functools.lru_cache(maxsize=None)
    def estimated_total(self):
        return self.elapsed + self.estimate_from()

    def estimate_from(self):
        e = 0
        p = (self.pos,) + self.goals
        for i in range(len(p) - 1):
            s = p[i]
            t = p[i + 1]
            e += abs(s[0] - t[0]) + abs(s[1] - t[1])

        return e

    def __lt__(a, b):
        return a.estimated_total() < b.estimated_total()

def main():
    inp = open(sys.argv[1])
    map = np.genfromtxt(inp, delimiter=1, dtype='<U1', comments=None)

    m, n = map.shape

    assert map[0, 1] == '.'
    assert map[m-1, n-2] == '.'

    # Blizzards heading each direction
    blizzards = {
        'w': map[1:m-1, 1:n-1] == '<',
        'e': map[1:m-1, 1:n-1] == '>',
        'n': map[1:m-1, 1:n-1] == '^',
        's': map[1:m-1, 1:n-1] == 'v',
    }

    s = (0, 1)
    g = (m - 1, n - 2)
    start = State(pos=(0, 1), goals=(g, s, g), elapsed=0)
    final = search(map, start, blizzards)
    print(final.elapsed)

def search(map, start, blizzards):
    """A* search"""

    m, n = map.shape

    visited = set(start)
    queue = [start]
    while queue:
        s = heapq.heappop(queue)
        dprint(f"popped {s}")
        if len(s.goals) == 0:
            return s

        for t in neighbor_states(s, map, blizzards):
            if t in visited:
                continue
            dprint(f"  neighbor {t} pushed")

            visited.add(t)
            heapq.heappush(queue, t)

    return None

def neighbor_states(s, map, blizzards):
    m, n = map.shape
    i, j = s.pos

    def state_at(u, v):
        if (u, v) == s.goals[0]:
            return State(pos=(u, v), goals=s.goals[1:], elapsed=s.elapsed + 1)
        else:
            return State(pos=(u, v), goals=s.goals, elapsed=s.elapsed + 1)

    candidates = []
    if i > 0:
        candidates.append(state_at(i - 1, j))
    if j > 0:
        candidates.append(state_at(i, j - 1))
    if i < m - 1:
        candidates.append(state_at(i + 1, j))
    if j < n - 1:
        candidates.append(state_at(i, j + 1))
    candidates.append(State(pos=s.pos, goals=s.goals, elapsed=s.elapsed + 1))

    mm = m - 2
    nn = n - 2
    for c in candidates:
        ci, cj = c.pos
        if map[ci, cj] == '#':
            continue

        if ci in (0, m - 1):
            # No blizzards
            yield c
            continue
        if cj in (0, n - 1):
            yield c
            continue

        # The position of blizzards is uniquely determined by the time.
        # There is a southward-moving blizzard at i, j at time t ==>
        #   There was a blizzard at (u = i - t), v at time 0.
        # (Subtract 1 for north and west borders.)
        if blizzards['n'][(ci - 1 + c.elapsed) % mm, cj - 1]:
            continue
        if blizzards['s'][(ci - 1 - c.elapsed) % mm, cj - 1]:
            continue
        if blizzards['w'][ci - 1, (cj - 1 + c.elapsed) % nn]:
            continue
        if blizzards['e'][ci - 1, (cj - 1 - c.elapsed) % nn]:
            continue

        yield c

main()
