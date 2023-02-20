#!/usr/bin/env python3

import io
import os
import numpy as np
import re
import signal
import sys
from pprint import pprint
from collections import namedtuple

import sympy

DEBUG = os.environ.get("DEBUG")

def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

def dpretty(*args, **kwargs):
    if DEBUG:
        pprint(*args, **kwargs)

def main():
    inp = open(sys.argv[1]).read()

    vals = {}
    for line in io.StringIO(inp):
        name, expr = line.split(": ")
        vals[name] = expr.strip()

    def _eval(name):
        expr = vals[name]
        if name == "root":
            expr_lhs, expr_rhs = expr.split("+")
            lhs = _eval(expr_lhs.strip())
            rhs = _eval(expr_rhs.strip())
            return sympy.Eq(lhs, rhs)
        elif name == "humn":
            expr = vals[name] = sympy.symbols('humn')
        elif type(expr) == str:
            names = re.findall(r"[a-z]{4}", expr)
            for n in names:
                _eval(n)
            expr = vals[name] = eval(expr, None, vals)

        return expr

    e = _eval("root")
    s = sympy.solve(e, vals['humn'])
    print(s)

main()
