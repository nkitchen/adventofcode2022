#!/usr/bin/env python3

import io
import os
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

def main():
    inp = open(sys.argv[1]).read()

    vars = {}
    for m in re.finditer(r"[a-z]{4}", inp):
        name = m.group(0)
        if name not in vars:
            vars[name] = intvar(-2**31, 2**31, name=name)

    model = Model()
    for line in io.StringIO(inp):
        if line.startswith("root:"):
            expr = line[5:].replace("+", "==")
            model += eval(expr, None, vars)
        elif line.startswith("humn:"):
            continue
        else:
            expr = line.replace(":", "==")
            expr = expr.replace("/", "//")
            model += eval(expr, None, vars)

    r = model.solve()
    assert r

    print(vars['humn'].value())

main()
