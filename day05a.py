#!/usr/bin/env python3

import os
import numpy as np
import re
import sys
from pprint import pprint

DEBUG = os.environ.get("DEBUG")

def main():
    inp = open(sys.argv[1])
    lines = [line.rstrip() for line in inp]

    i = lines.index("")
    stack_lines = lines[:i]
    move_lines = lines[i + 1:]
    
    # The algorithm doesn't lend itself to array programming (ordinary Python lists are better),
    # but I can still use numpy to parse the stacks.

    # Pad to same width.
    n = max(len(line) for line in stack_lines)
    stack_lines = [f"{line:{n}}" for line in stack_lines]

    stack_grid = np.genfromtxt(stack_lines, dtype='<U1', delimiter=1)
    stack_labels = stack_grid[-1]
    stack_cols = np.where(stack_labels != ' ')[0]

    stacks = {}
    for i, label in enumerate(stack_labels[stack_cols]):
        label = int(label)
        sa = stack_grid[-2::-1, stack_cols[i]]
        s = ''.join(sa).rstrip()
        stacks[label] = list(s)

    for line in move_lines:
        k, src, dst = map(int, re.findall(r"\d+", line))
        stacks[dst] += reversed(stacks[src][-k:])
        stacks[src] = stacks[src][:-k]

    tops = [stacks[label][-1] for label in sorted(stacks)]
    print(''.join(tops))

main()
