#!/usr/bin/env python3

import sys
import numpy as np
from math import sqrt

#read input
data = sys.stdin.buffer.read()
A = np.frombuffer(data, dtype=float)
D, Q = np.split(A, 2)
n = int(sqrt(len(D)))
D = D.reshape(n,n)
Q = Q.reshape(n,n)
B = np.matmul(D, Q.T)

#write output
sys.stdout.buffer.write(B.tobytes())

