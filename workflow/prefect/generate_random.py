#!/usr/bin/env python3

import sys
import numpy as np

#read input
n = int(sys.argv[1])
A = np.random.random((n, n))

#write output
sys.stdout.buffer.write(A.tobytes())

