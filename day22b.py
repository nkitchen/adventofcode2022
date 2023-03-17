#!/usr/bin/env python3

import io
import itertools
import os
import numpy as np
import re
import sys
from pprint import pprint
from collections import namedtuple

DEBUG = os.environ.get("DEBUG")
SHOW = os.environ.get("SHOW")

facing_chr = {
    (0, 1): '>',
    (0, -1): '<',
    (1, 0): 'V',
    (-1, 0): '^',
}

facing_num = {
    (0, 1): 0,
    (0, -1): 2,
    (1, 0): 1,
    (-1, 0): 3,
}

Facet = namedtuple('Facet', 'normal m offset')

def main():
    inp = open(sys.argv[1]).read()

    map, path_descr = inp.split("\n\n")

    # Pad to same width.
    map_lines = map.split('\n')
    n = max(len(line) for line in map_lines)
    map_lines = [f"{line:{n}}" for line in map_lines]

    tiles = np.array([np.array(list(line)) for line in map_lines])
    trail = tiles.copy()

    # Find the cube side length.
    tiled = (tiles != ' ')
    s = tiled.sum(axis=0).min()

    def show():
        if not SHOW:
            return
        for row in trail:
            print(' '.join(c for c in row))
        print()

    # Construct the mapping between xyz coordinates and tile indices.
    # Each face of the cube has its own relationship:
    #  m @ (x, y, z) + offset = (i, j)

    # normal=[0 0 1] m=[[0 -1 0] [1 0 0]] anchor=[0 8]
    # xyz=[0 3 4] ij=[0 8]
    # offset = -m @ xyz + ij = [3 0] + [0 8] = [3 8]

    # xyz=[3 0 4] ij=[3 11]
    # -m @ xyz + ij = [0 -3] + [3 11] = [3 8]
    facet_by_normal = {}

    # Find first "anchor": a local origin -- the upper-left tile of the face.
    anchor = np.array([0, 0])
    while tiles[tuple(anchor)] == ' ':
        anchor[1] += 1

    # Top face
    normal = np.array([0, 0, 1])
    m = np.array([[0, -1, 0], [1, 0, 0]])
    xyz = np.array([0, s - 1, s])
    offset = anchor - m @ xyz
    facet = Facet(normal, m, offset)
    facet_by_normal[tuple(normal)] = facet

    # Find other faces by adjacency on the tile map.
    Entry = namedtuple('Entry', 'facet xyz anchor')
    q = [Entry(facet, xyz, anchor)]
    while q:
        entry = q[0]
        q = q[1:]

        facet = entry.facet
        i, j = entry.anchor
        if j - s >= 0 and tiles[i, j - s] != ' ':
            nxyz = entry.xyz - facet.m[1] - s * facet.normal
            nanchor = np.array([i, j - s])
            nnormal = -facet.m[1]
            nm = facet.m.copy()
            nm[1] = facet.normal
            noffset = nanchor - nm @ nxyz
            nfacet = Facet(nnormal, nm, noffset)
            if tuple(nnormal) not in facet_by_normal:
                facet_by_normal[tuple(nnormal)] = nfacet
                q.append(Entry(nfacet, nxyz, nanchor))
        if j + s < tiles.shape[1] and tiles[i, j + s] != ' ':
            nxyz = entry.xyz + s * facet.m[1] - facet.normal
            nanchor = np.array([i, j + s])
            nnormal = facet.m[1]
            nm = facet.m.copy()
            nm[1] = -facet.normal
            noffset = nanchor - nm @ nxyz
            nfacet = Facet(nnormal, nm, noffset)
            if tuple(nnormal) not in facet_by_normal:
                facet_by_normal[tuple(nnormal)] = nfacet
                q.append(Entry(nfacet, nxyz, nanchor))
        if i + s < tiles.shape[0] and tiles[i + s, j] != ' ':
            nxyz = entry.xyz + s * facet.m[0] - facet.normal
            nanchor = np.array([i + s, j])
            nnormal = facet.m[0]
            nm = facet.m.copy()
            nm[0] = -facet.normal
            noffset = nanchor - nm @ nxyz
            nfacet = Facet(nnormal, nm, noffset)
            if tuple(nnormal) not in facet_by_normal:
                facet_by_normal[tuple(nnormal)] = nfacet
                q.append(Entry(nfacet, nxyz, nanchor))

    xyz = np.array([0, s - 1, s])
    normal = np.array([0, 0, 1])
    facet = facet_by_normal[tuple(normal)]
    heading = facet.m[1]

    ij = facet.m @ xyz + facet.offset
    facing = facet.m @ heading
    trail[tuple(ij)] = facing_chr[tuple(facing)]

    path_descr = path_descr.strip()
    path_index = 0
    path_re = re.compile(r"(\d+)|([RL])")
    while path_index < len(path_descr):
        m = path_re.match(path_descr, path_index)
        assert m
        path_index = m.end()

        if (d := m.group(1)):
            d = int(d)
            for k in range(d):
                nxyz = (xyz + heading)
                if ((0 <= nxyz) & (nxyz < s)).sum() >= 2:
                    # Still on the same face
                    nfacet = facet
                    nheading = heading
                else:
                    # Past an edge
                    nnormal = heading
                    nfacet = facet_by_normal[tuple(nnormal)]
                    nxyz -= facet.normal
                    nheading = -facet.normal

                nij = nfacet.m @ nxyz + nfacet.offset
                if (t := tiles[tuple(nij)]) == '.':
                    xyz = nxyz
                    heading = nheading
                    facet = nfacet

                    facing = facet.m @ heading
                    trail[tuple(nij)] = facing_chr[tuple(facing)]
                else:
                    assert t == '#'
                    break
        elif (rot := m.group(2)) == 'L':
            heading = -np.cross(heading, facet.normal)
            ij = facet.m @ xyz + facet.offset
            facing = facet.m @ heading
            trail[tuple(ij)] = facing_chr[tuple(facing)]
        else:
            assert rot == 'R'
            heading = np.cross(heading, facet.normal)
            ij = facet.m @ xyz + facet.offset
            facing = facet.m @ heading
            trail[tuple(ij)] = facing_chr[tuple(facing)]

    show()

    i, j = facet.m @ xyz + facet.offset
    facing = facet.m @ heading
    password = 1000 * (i + 1) + 4 * (j + 1) + facing_num[tuple(facing)]
    print(password)

main()
