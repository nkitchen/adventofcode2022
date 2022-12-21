#!/usr/bin/env python3

import io
import itertools
import os
import numpy as np
import re
import sys
from pprint import pprint
from collections import defaultdict

DEBUG = os.environ.get("DEBUG")

def main():
    index_seq = itertools.count()
    def next_index():
        return next(index_seq)
    
    # Maps full paths to index values 0...n
    index = defaultdict(next_index)

    size_by_path = defaultdict(int)

    cwd = None
    inp = open(sys.argv[1]).read()
    for cmd_out in re.findall(r"(?sm)^[$] ([^$]*)", inp):
        cmd_lines = io.StringIO(cmd_out)

        line = next(cmd_lines)
        cmd = line.split()
        if cmd[0] == "cd":
            w = cmd[1]
            if w == '/':
                cwd = ()
            elif w == '..':
                cwd = cwd[:-1]
            else:
                cwd += (w,)

            i = index[cwd]
            size_by_path[cwd] = 0
        elif cmd[0] == 'ls':
            for line in cmd_lines:
                s, name = line.split()
                path = cwd + (name,)
                if s != 'dir':
                    size_by_path[path] = int(s)
                _ = index[path]

    n = len(index)
    # size_part[i][j] is 1 if the size of path with index i is included in
    # the size of path with index j.
    # As a special case, size_part[i][i] is 1 for non-directories i (so that
    # their entries in the size vector stay unchanged).
    size_part = np.zeros((n, n), dtype=int)
    for path, j in index.items():
        if len(path) == 0:
            continue
        parent = path[:-1]
        i = index[parent]
        size_part[i][j] = 1

    size = np.zeros((n), dtype=int)
    for path, m in size_by_path.items():
        i = index[path]
        if m != 0:
            size_part[i][i] = 1
            size[i] = m
    dir = (size == 0)

    # One multiplication of size_part by size brings the sums up one level.
    while (((new_size := np.matmul(size_part, size)) != size).any()):
        size = new_size

    if DEBUG:
        for path in sorted(index):
            i = index[path]
            print(path, size[i])

    total_space = 70000000
    space_needed = 30000000

    used = size[index[()]]
    unused = total_space - used

    dir_size = size[dir]
    enough = dir_size + unused >= space_needed
    print(dir_size[enough].min())

main()
