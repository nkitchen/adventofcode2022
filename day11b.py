#!/usr/bin/env python3

import io
import os
import numpy as np
import re
import sys
from pprint import pprint

DEBUG = os.environ.get("DEBUG")

pattern = r"""Monkey (?P<id>\d+):
  Starting items: (?P<items>\d+(?:, \d+)*)
  Operation: new = (?P<inspect_expr>.*)
  Test: divisible by (?P<divisor>\d+)
    If true: throw to monkey (?P<true_throw>\d+)
    If false: throw to monkey (?P<false_throw>\d+)
"""

class Monkey:
    def __str__(self):
        return f"Monkey {self.id}: {self.items}"

def main():
    inp = open(sys.argv[1]).read()

    monkeys = []
    for m in re.finditer(pattern, inp):
        monkey = Monkey()
        monkey.id = int(m.group('id'))
        monkey.items = np.loadtxt([m.group('items')], delimiter=', ', dtype=np.int64)
        monkey.inspect_expr = m.group('inspect_expr')
        monkey.divisor = int(m.group('divisor'))
        monkey.true_throw = int(m.group('true_throw'))
        monkey.false_throw = int(m.group('false_throw'))

        monkeys.append(monkey)

    for i, monkey in enumerate(monkeys):
        assert monkey.id == i

    divisors = np.array([m.divisor for m in monkeys], dtype=np.int64)
    modulus = divisors.prod()

    n = len(monkeys)
    inspections = np.zeros((n,), dtype=int)

    for round in range(10000):
        for monkey in monkeys:
            old = monkey.items
            items = eval(monkey.inspect_expr) % modulus
            inspections[monkey.id] += len(monkey.items)
            i = (items % monkey.divisor == 0)
            t = monkey.true_throw
            f = monkey.false_throw
            monkeys[t].items = np.hstack((monkeys[t].items, items[i]))
            monkeys[f].items = np.hstack((monkeys[f].items, items[~i]))
            monkey.items = np.array([], dtype=np.int64)

    business = np.sort(inspections)[-2:].prod()
    print(business)

main()
