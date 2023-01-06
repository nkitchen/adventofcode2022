import re
import fileinput

print("graph {")

for line in fileinput.input():
    if (m := re.search(r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*\S)",
                       line)):
        v = m.group(1)
        rate = m.group(2)
        nbrs = m.group(3).split(", ")
        print(f'  {v} [label="{v}\\n{rate}"];')
        for w in nbrs:
            if v < w:
                print(f'  {v} -- {w};')

print("}")

