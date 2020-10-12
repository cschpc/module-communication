#!/usr/bin/env python

import sys
from time import sleep
import numpy as np
from mpi4py import MPI
from utility import init_sockets, send_array, recv_array

class ParallelModeler:

    def __init__(self, source, destination, comm):
        if comm.rank == 0:
            self.receiver, self.sender = init_sockets(source, destination)
        self.comm = comm

    def compute(self, data):
        #do stuff
        result = data + 40 * self.comm.rank
        result = self.comm.reduce(result, op=MPI.SUM, root=0)
        return result

    def busy_loop(self):
        while True:
            try:
                # data = self.receiver.recv()
                if self.comm.rank == 0:
                    data = recv_array(self.receiver)
                    print("Data in", self.__class__.__name__, data)
                    req = []
                    for i in range(1, self.comm.size):
                        req.append(self.comm.isend(data, dest=i))
                    MPI.Request.waitall(req)
                    # self.comm.bcast(data, root=0)
                else:
                    # data = self.comm.bcast(None, root=0)
                    while not self.comm.iprobe(source=0):
                        sleep(3)
                    data = self.comm.recv(source=0)
                        
                result = self.compute(data)
                # self.sender.send(result)
                if self.comm.rank == 0:
                    send_array(self.sender, result)
            except KeyboardInterrupt:
                if self.comm.rank == 0:
                    print('Module {} exiting'.format(self.__class__.__name__))
                break


def main(source, destination):

    comm = MPI.COMM_WORLD
    modeler = ParallelModeler(source, destination, comm)
    modeler.busy_loop()

if __name__ == '__main__':
    source, destination = sys.argv[1], sys.argv[2]
    main(source, destination)
