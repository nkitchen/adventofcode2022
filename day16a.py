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
    valves = set(v for v, r in rate.items() if r > 0)

    # f(S): max flow achievable by opening valves in set S
    # t(S): minutes used to open the valves in S to achieve f(S)
    # d(S): the last valve in S opened when achieving f(S)
    #
    # f({}) = 0
    # t({}) = 0
    # d({}) = AA
    #
    # f(S) = max(f(S - {v}) + (30 - t(S - {v}) - shortest[d(S - {v}), v] - 1) * rate[v]
    #            for v in S)
    # t(S) = t(S - {v}) + shortest[d(S - {v}), v] + 1
    #        for v = arg max f(S)
    # d(S) = v, arg max f(S)
    
    FlowData = namedtuple('FlowData', 'flow minutes_used last_node')

    @functools.lru_cache(maxsize=None)
    def search(s):
        if DEBUG:
            print(f"search({sorted(s)})...")

        if not s:
            return FlowData(0, 0, 'AA')

        best = None
        for v in s:
            r = search(s - frozenset([v]))
            i = vid[r.last_node]
            j = vid[v]
            t = r.minutes_used + int(shortest[i, j]) + 1

            if t >= 30:
                d = r
            else:
                f = r.flow + (30 - t) * rate[v] 
                d = FlowData(f, t, v)

            if best is None or d.flow > best.flow:
                best = d

        if DEBUG:
            print(f"search({sorted(s)}) = {best}")

        return best

    r = search(frozenset(valves))
    print(r.flow)

main()
