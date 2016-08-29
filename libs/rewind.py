#!/usr/bin/python
#
# Debug script which can restore initial condition of the
# 'spelling.txt' file, input argument *threshold* contains
# number of lines to keep.

import sys

threshold = sys.argv[1]

spell = open('spelling.txt', 'r+')
lines = spell.readlines()

count = 1
spell.seek(0)

for line in lines:
    if count <= int(threshold):
        spell.write(line)
    count += 1
spell.truncate()

spell.close()
