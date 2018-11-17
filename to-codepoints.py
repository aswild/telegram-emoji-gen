#!/usr/bin/env python3

import sys

translate = lambda e: '-'.join('%x'%ord(c) for c in e)

if len(sys.argv) > 1:
    infile = open(sys.argv[1], 'r')
else:
    infile = sys.stdin

for line in infile.read().splitlines():
    print(translate(line))

infile.close()
