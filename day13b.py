#!/usr/bin/env python3

import functools
import io
import os
import numpy as np
import re
import sys
from pprint import pprint

DEBUG = os.environ.get("DEBUG")

def main():
    inp = open(sys.argv[1])

    packets = []
    for line in inp:
        s = line.strip()
        if not s:
            continue
        packets.append(eval(s))

    packets.append([[2]])
    packets.append([[6]])

    packets.sort(key=functools.cmp_to_key(compare))
    i = 1 + packets.index([[2]])
    j = 1 + packets.index([[6]])
    print(i * j)

def compare(a, b):
    if type(a) == type(b) == int:
        return a - b

    if type(a) == type(b) == list:
        m = len(a)
        n = len(b)
        for i in range(max(m, n)):
            if i < m and i >= n:
                return 1
            if i >= m and i < n:
                return -1
            c = compare(a[i], b[i])
            if c == 0:
                continue
            return c

        return 0

    if type(a) == int:
        return compare([a], b)
    else:
        return compare(a, [b])

main()
