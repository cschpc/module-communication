#!/usr/bin/env python3

import sys
import numpy as np
from math import sqrt

#read input
data = sys.stdin.buffer.read()
C = np.frombuffer(data, dtype=float)
# raise RuntimeError('Failure')
n = int(sqrt(len(C)))
C = C.reshape(n,n)
eigvals = np.linalg.eigvals(C)
eigvals.sort()
#write output
sys.stdout.buffer.write(eigvals.tobytes())

