#!/usr/bin/env python3

import os
import numpy as np
import sys
from pprint import pprint

DEBUG = os.environ.get("DEBUG")
SHOW = os.environ.get("SHOW")

def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

def main():
    inp = open(sys.argv[1])

    snafus = np.array(list(line.strip() for line in inp))

    conv = np.frompyfunc(snafu_to_dec, 1, 1)

    dec = conv(snafus)
    t = dec_to_snafu(dec.sum())
    print(t)

digit_value = {
    '0': 0,
    '1': 1,
    '2': 2,
    '-': -1,
    '=': -2,
}

def snafu_to_dec(s):
    d = 0
    for digit in s:
        d *= 5
        d += digit_value[digit]
    return d

snafu_digits = '012=-'

def dec_to_snafu(dec):
    digits = []
    while dec > 0:
        p = dec % 5
        digits.append(snafu_digits[p])
        if p > 2:
            dec //= 5
            dec += 1
        else:
            dec //= 5

    return ''.join(reversed(digits))

main()
