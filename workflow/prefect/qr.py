#!/usr/bin/env python3

import sys
import numpy as np
from math import sqrt

#read input
data = sys.stdin.buffer.read()
A = np.frombuffer(data, dtype=float)
n = int(sqrt(len(A)))
A = A.reshape(n,n)
Q, R = np.linalg.qr(A)

#write output
sys.stdout.buffer.write(Q.tobytes())

