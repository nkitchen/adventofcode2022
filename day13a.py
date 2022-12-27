#!/usr/bin/env python3

import io
import os
import numpy as np
import re
import sys
from pprint import pprint

DEBUG = os.environ.get("DEBUG")

def main():
    inp = open(sys.argv[1]).read()

    in_order = []
    pairs = inp.split('\n\n')
    for pair in pairs:
        lists = pair.split('\n')
        a = eval(lists[0])
        b = eval(lists[1])
        in_order.append(compare(a, b) <= 0)

    x = np.array(in_order)
    i = x.nonzero()[0]
    print((i + 1).sum())

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
