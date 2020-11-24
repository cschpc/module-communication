#!/usr/bin/env python3

import sys
import numpy as np

#read input
n = int(sys.argv[1])
eigvals = np.arange(0, n, dtype=float)
D = np.diag(eigvals)

#write output
sys.stdout.buffer.write(D.tobytes())

