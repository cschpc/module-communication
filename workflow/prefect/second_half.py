#!/usr/bin/env python3

import sys
import numpy as np
from math import sqrt

#read input
data = sys.stdin.buffer.read()
A = np.frombuffer(data, dtype=float)
Q, B = np.split(A, 2)
n = int(sqrt(len(Q)))
Q = Q.reshape(n,n)
B = B.reshape(n,n)
C = np.matmul(Q, B)

#write output
sys.stdout.buffer.write(C.tobytes())

