#!/usr/bin/env python

import sys
import numpy as np
from base_modeler import BaseModeler

class Modeler(BaseModeler):

    def compute(self, data):
        #do stuff
        result = data + 10
        return result

def main(source, destination):

    modeler = Modeler(source, destination)
    modeler.busy_loop()

if __name__ == '__main__':
    source, destination = sys.argv[1], sys.argv[2]
    main(source, destination)
