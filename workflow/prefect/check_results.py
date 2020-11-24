#!/usr/bin/env python3

import sys
import numpy as np
from math import sqrt

#read input
data = sys.stdin.buffer.read()
eigvals = np.frombuffer(data, dtype=float)
n = len(eigvals)
correct = np.arange(0, n, dtype=float)
check = np.abs(eigvals - correct).max() < 0.0001
print("Check results:", check)

