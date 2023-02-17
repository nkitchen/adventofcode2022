#!/usr/bin/env python3

import io
import os
import numpy as np
import re
import signal
import sys
from pprint import pprint
from collections import namedtuple

DEBUG = os.environ.get("DEBUG")

def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

def dpretty(*args, **kwargs):
    if DEBUG:
        pprint(*args, **kwargs)

"""
Approach:
    A state is (t, m, r):
        t: minutes after start
        m: vector of mineral inventory
        r: vector of robot inventory

    Starting from (t=0, m=(0, 0, 0, 0), r=(1, 0, 0, 0)),
    find states with t <= 24 that are reachable by
    actions of building each possible kind of robot.

    For example, from (t=5, m=(2, 4, 0, 0), r=(1, 2, 0, 0)),
    with blueprint (4, 2, 3+14, 2+7),
    one possible action is to build a clay robot next.
    The mineral inventory is not enough yet (ore < 2),
    but the robot inventory has an ore robot,
    so we can wait for enough ore to be collected.
       requirement for ore: 2 - 1 = 1
       ceil(1 ore / 2 robots) = 1 minute needed
       Add 1 minute for building.
       t' = t + 2 = 7
       m' = m + 2 * r - (0, 2, 0, 0)
       r' = r + (0, 1, 0, 0)
"""

T_MAX = 24

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3

def main():
    inp = open(sys.argv[1])

    blueprints = read_blueprints(inp)
    qualities = [id * max_geodes(bp) for id, bp in blueprints.items()]
    print(qualities.sum())

kind_index = {
    'ore': ORE,
    'clay': CLAY,
    'obsidian': OBSIDIAN,
    'geode': GEODE,
}

State = namedtuple('State', 'elapsed mineral robot')

def freeze(state):
    return (state.elapsed, tuple(state.mineral), tuple(state.robot))

def max_geodes(blueprint):
    start = State(0, np.array([0.0, 0.0, 0.0, 0.0]), np.array([1.0, 0.0, 0.0, 0.0]))

    visited = set()
    visited.add(freeze(start))

    q = [start]

    def sig_status(signum, frame):
        print(f"q: {len(q)} visited: {len(visited)}", file=sys.stderr)
        sys.stderr.flush()
    signal.signal(signal.SIGUSR1, sig_status)

    while q:
        s = q[0]
        q = q[1:]

        # Each robot kind
        for r in range(blueprint.shape[0]):
            req = blueprint[r]
            if (s.mineral >= req).all():
                # I have enough material.
                nt = s.elapsed + 1
                nm = s.mineral + s.robot - blueprint[r]
                nr = s.robot.copy()
                nr[r] += 1
            elif (s.robot[req > 0] > 0).all():
                # I have all the robots I need to get the required material.
                i = req > 0
                dm = req[i] - s.mineral[i]
                dt = np.ceil(dm / s.robot[i]).max()

                nt = s.elapsed + dt + 1
                nm = s.mineral + (dt + 1) * s.robot - blueprint[r]
                nr = s.robot.copy()
                nr[r] += 1
            else:
                continue

            if nt > T_MAX:
                continue

            ns = State(nt, nm, nr)
            nst = freeze(ns)
            if nst not in visited:
                visited.add(nst)
                q.append(ns)

                dprint(len(q), len(visited))

    geode_counts = []
    for s in visited:
        dt = T_MAX - s.elapsed
        g = s.mineral[GEODE] + dt * s.robot[GEODE]
        geode_counts.append(g)
    return max(geode_counts)

def read_blueprints(f):
    blueprints = {}
    for line in f:
        m = re.search(r"Blueprint (\d+):", line)
        assert m
        id = int(m.group(1))

        b = np.zeros((4,4), dtype=float)
        for m in re.finditer(r"Each (\w+) robot costs (.*?)[.]", line):
            robot_kind = m.group(1)
            r = kind_index[robot_kind]
            costs = m.group(2)
            for m in re.finditer(r"(\d+) (\w+)", costs):
                x = int(m.group(1))
                mineral_kind = m.group(2)
                m = kind_index[mineral_kind]
                b[r, m] = x
        blueprints[id] = b

    return blueprints

main()
