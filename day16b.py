#!/usr/bin/env python3

import functools
import io
import os
import numpy as np
import re
import sys
import time
from pprint import pprint
from collections import defaultdict
from collections import namedtuple
from scipy.sparse import csgraph

DEBUG = os.environ.get("DEBUG")
DISPLAY = os.environ.get("DISPLAY")

MAX_MINUTES = 26

def main():
    full_adj = {}
    rate = {}

    inp = open(sys.argv[1])
    for line in inp:
        if not (m := re.search(r"Valve (\w+) has flow rate=(\d+); "
                               r"tunnels? leads? to valves? (.*\S)",
                               line)):
            continue

        u = m.group(1)
        r = int(m.group(2))
        vv = m.group(3).split(", ")
        full_adj[u] = vv
        rate[u] = r

    # Assign indices to nodes.
    vid = defaultdict()
    vid.default_factory = lambda: len(vid)

    n = len(full_adj)

    # Find shortest distances between nodes.
    adj = np.zeros((n, n), dtype=int)
    for u, vv in full_adj.items():
        i = vid[u]
        for v in vv:
            j = vid[v]
            adj[i, j] = 1
    shortest = csgraph.floyd_warshall(adj, directed=False)

    # Reduced node set: non-zero flow rate or AA
    valves = frozenset(v for v, r in rate.items() if r > 0)

    # f(S, v): max flow achievable by opening the valves in set S and then v
    # t(S, v): minutes used to achieve f(S, v)
    #
    # f({}, AA) = 0
    # t({}, AA) = 0
    
    FlowData = namedtuple('FlowData', 'flow minutes_used')

    @functools.lru_cache(maxsize=None)
    def search(s, v):
        if DEBUG:
            print(f"search({sorted(s)}, {v})...")

        if not s:
            assert v != 'AA'
            i = vid['AA']
            j = vid[v]
            t = int(shortest[i, j]) + 1
            if t >= MAX_MINUTES:
                return None

            f = (MAX_MINUTES - t) * rate[v]
            d = FlowData(f, t)
            if DEBUG:
                print(f"search({sorted(s)}, {v}) = {d}")
            return d

        best = None
        for u in s:
            r = search(s - frozenset([u]), u)
            if r is None:
                continue

            i = vid[u]
            j = vid[v]
            t = r.minutes_used + int(shortest[i, j]) + 1

            if t >= MAX_MINUTES:
                continue

            f = r.flow + (MAX_MINUTES - t) * rate[v] 
            d = FlowData(f, t)
            if DEBUG:
                print(f"  check: ({f - r.flow}, {t - r.minutes_used}, {v}) + {r}")
            if (best is None or d.flow > best.flow or
                (d.flow == best.flow and d.minutes_used < best.minutes_used)):
                best = d

        if DEBUG:
            print(f"search({sorted(s)}, {v}) = {best}")

        return best

    best = None
    for s1 in subsets(valves):
        best1 = None
        for u in s1:
            r1 = search(s1 - frozenset([u]), u)
            if r1 is None:
                continue
            if best1 is None or r1.flow > best1:
                best1 = r1.flow
        if best1 is None:
            continue

        for s2 in subsets(valves - s1):
            best2 = None
            for v in s2:
                r2 = search(s2 - frozenset([v]), v)
                if r2 is None:
                    continue
                if best2 is None or r2.flow > best2:
                    best2 = r2.flow
            if best2 is None:
                continue

            f = best1 + best2
            if best is None or f > best:
                if DEBUG:
                    print("best:")
                    print(f"  {r1}")
                    print(f"  {r2}")
                best = f

    print(best)

def subsets(s):
    a = list(s)
    n = len(a)
    for b in range(1, 1 << n):
        p = set(a[i] for i in range(n)
                if b & (1 << i))
        yield frozenset(p)

main()
