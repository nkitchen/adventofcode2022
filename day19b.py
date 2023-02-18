#!/usr/bin/env python3

import io
import os
import natsort
import numpy as np
import re
import signal
import sys
from pprint import pprint
from collections import namedtuple

from cpmpy import *

DEBUG = os.environ.get("DEBUG")

def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

def dpretty(*args, **kwargs):
    if DEBUG:
        pprint(*args, **kwargs)

T_MAX = 32

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3

def main():
    inp = open(sys.argv[1])

    blueprints = read_blueprints(inp)

    # Check structure of mineral requirements.
    for id, bp in blueprints.items():
        assert (bp[bp > 0] > 1).all()

        for r in range(bp.shape[0]):
            req = bp[r][bp[r] > 0]
            assert sorted(req) == list(req)

    r = 1
    for id in natsort.natsorted(blueprints)[:3]:
        bp = blueprints[id]
        g = max_geodes(bp)
        print(g)
        r *= g

    print(r)

kind_index = {
    'ore': ORE,
    'clay': CLAY,
    'obsidian': OBSIDIAN,
    'geode': GEODE,
}

def max_geodes(blueprint):
    model = Model()

    req = cpm_array(np.vstack((blueprint, np.array([0, 0, 0, 0]))))

    robot = intvar(0, T_MAX + 1, shape=(T_MAX + 1, 4), name="r")
    mineral = intvar(0, (T_MAX + 1)**2, shape=(T_MAX + 1, 4), name="m")
    build = intvar(0, 4, shape=T_MAX, name="b")

    # Initial conditions
    model += (robot[0, ORE] == 1)
    model += (robot[0, CLAY] == 0)
    model += (robot[0, OBSIDIAN] == 0)
    model += (robot[0, GEODE] == 0)

    for m in range(4):
        model += (mineral[0, m] == 0)

    # I can only use minerals that I have.
    for t in range(0, T_MAX):
        for m in range(0, 4):
            model += (mineral[t, m] >= req[build[t], m])

        # Collection
        for t in range(0, T_MAX):
            for m in range(4):
                model += (mineral[t + 1, m] == mineral[t, m] + robot[t, m] - req[build[t], m])

        # Robot building
        for t in range(0, T_MAX):
            for r in range(4):
                model += (build[t] == r).implies(robot[t + 1, r] == 1 + robot[t, r])
                model += (build[t] != r).implies(robot[t + 1, r] == robot[t, r])

    model.maximize(mineral[T_MAX, GEODE])

    try:
        if model.solve():
            dprint(np.transpose(robot.value()))
            dprint(np.transpose(mineral.value()))
            return mineral.value()[T_MAX, GEODE]
        else:
            return 0
    finally:
        sys.stderr.write(".")
        sys.stderr.flush()

def read_blueprints(f):
    blueprints = {}
    for line in f:
        m = re.search(r"Blueprint (\d+):", line)
        assert m
        id = int(m.group(1))

        b = np.zeros((4,4), dtype=int)
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
