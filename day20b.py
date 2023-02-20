#!/usr/bin/env python3

import io
import os
import numpy as np
import re
import signal
import subprocess
import sys
import tempfile
from pprint import pprint
from dataclasses import dataclass
from typing import *

DEBUG = os.environ.get("DEBUG")

def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

def dpretty(*args, **kwargs):
    if DEBUG:
        pprint(*args, **kwargs)

key = 811589153

def main():
    inp = open(sys.argv[1]).read()

    numbers = [int(x) * key for x in inp.split()]
    i0 = numbers.index(0)

    tree = make_tree(numbers)
    tree.dshow()

    nodes = list(tree.nodes())
    # Check structure.
    for i, n in enumerate(nodes):
        p = n.pos()
        assert i == p
    n0 = nodes[i0]

    for t in range(10):
        for n in nodes:
            if n.value == 0:
                continue

            i = n.pos()
            tree = n.remove()

            j = (i + n.value - 1) % (len(numbers) - 1) + 1
            tree.insert(j, n)
            tree.dshow()

    i0 = n0.pos()
    s = 0
    for d in [1000, 2000, 3000]:
        j = (i0 + d) % len(numbers)
        n = tree.at(j)
        s += n.value
    print(s)

@dataclass
class Node:
    value: Any
    left: Optional['Node']
    right: Optional['Node']
    parent: Optional['Node'] = None
    size: int = 0

    def left_size(self):
        if self.left:
            return self.left.size
        else:
            return 0

    def right_size(self):
        if self.right:
            return self.right.size
        else:
            return 0

    def set_left(self, left):
        self.left = left
        if left:
            left.parent = self

    def set_right(self, right):
        self.right = right
        if right:
            right.parent = self

    # Returns the node's index in the sequence, that is, the number of
    # other nodes preceding it.
    def pos(self):
        i = self.left_size()

        n = self
        while n.parent:
            if n == n.parent.right:
                i += 1 + n.parent.left_size()
            n = n.parent

        return i

    def nodes(self):
        if self.left:
            yield from self.left.nodes()
        yield self
        if self.right:
            yield from self.right.nodes()

    def remove(self):
        # Rotate it down to a leaf.
        while self.left or self.right:
            rotate_left = (
                not self.left or
                self.left_size() <= self.right_size()
            )
            if rotate_left:
                p = self.parent
                n = self.right
                rl = n.left
                n.set_left(self)
                self.set_right(rl)

                if p:
                    if self == p.left:
                        p.set_left(n)
                    else:
                        p.set_right(n)
                else:
                    n.parent = None

                self.size = 1 + self.left_size() + self.right_size()
                n.size = 1 + self.size + n.right_size()
            else:
                p = self.parent
                n = self.left
                lr = n.right
                n.set_right(self)
                self.set_left(lr)

                if p:
                    if self == p.left:
                        p.set_left(n)
                    else:
                        p.set_right(n)
                else:
                    n.parent = None

                self.size = 1 + self.left_size() + self.right_size()
                n.size = 1 + n.left_size() + self.size

        # Detach.
        if (n := self.parent):
            if self == n.left:
                n.set_left(None)
            else:
                n.set_right(None)
            self.parent = None

            # Update sizes.
            while True:
                n.size = 1 + n.left_size() + n.right_size()
                if not n.parent:
                    return n
                n = n.parent
        else:
            return None

    def insert(self, i, n):
        assert 0 <= i <= self.size
        assert n.size == 1

        if i == 0 and not self.left:
            self.set_left(n)
        elif i <= self.left_size():
            self.left.insert(i, n)
        elif self.right:
            self.right.insert(i - self.left_size() - 1, n)
        else:
            self.set_right(n)
        self.size += 1

    def at(self, i):
        assert 0 <= i < self.size
        
        if i == self.left_size():
            return self
        if i < self.left_size():
            return self.left.at(i)
        return self.right.at(i - self.left_size() - 1)

    def root(self):
        n = self
        while n.parent:
            n = n.parent
        return n

    def dshow(self):
        if not DEBUG:
            return

        f = tempfile.NamedTemporaryFile('w')
        print("digraph {", file=f)
        print('ordering="out";', file=f)
        for n in self.nodes():
            print(f'n{id(n)} [label="{n.value}\\n={n.size}"];', file=f)
            if n.left:
                print(f'n{id(n)} -> n{id(n.left)} [label="L"];', file=f)
            if n.right:
                print(f'n{id(n)} -> n{id(n.right)} [label="R"];', file=f)
            if n.parent:
                print(f'n{id(n.parent)} -> n{id(n)} [dir=back, style=dashed];', file=f)
        print('}', file=f)
        f.flush()

        subprocess.run(f'xdot {f.name}', shell=True)

def make_tree(values):
    if len(values) == 0:
        return None

    m = len(values) // 2
    a = values[:m]
    b = values[m + 1:]
    left = make_tree(a)
    right = make_tree(b)

    n = Node(values[m], left, right)
    s = 1

    if left is not None:
        left.parent = n
        s += left.size
    if right is not None:
        right.parent = n
        s += right.size
    n.size = s

    return n

main()
