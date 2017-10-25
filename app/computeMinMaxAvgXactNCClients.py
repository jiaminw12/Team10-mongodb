#!/usr/bin/env python

from __future__ import division
import sys
import time
from decimal import *

throughputNum = []
filePath = '../app/throughput.txt';
with open(filePath, 'r+') as myFile:
	throughputNum = [Decimal(line.rstrip()) for line in myFile]

print(throughputNum)
max_value = max(throughputNum)
min_value = min(throughputNum)
avg_value = sum(throughputNum)/len(throughputNum)

print "Minimum transaction outputs: %f" % min_value
print "Maximum transaction outputs: %f" % max_value
print "Average transaction outputs: %f" % avg_value
