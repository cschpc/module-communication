#!/usr/bin/env python
import sys
import zmq
import numpy

def init_sockets(source, destination):

    context = zmq.Context()

    receiver = context.socket(zmq.PULL)
    receiver.bind(source)
    
    sender = context.socket(zmq.PUSH)
    sender.connect(destination)

    return receiver, sender

def send_array(socket, A, flags=0, copy=True, track=False):
    """send a numpy array with metadata"""
    md = dict(
        dtype = str(A.dtype),
        shape = A.shape,
    )
    socket.send_json(md, flags|zmq.SNDMORE)
    return socket.send(A, flags, copy=copy, track=track)

def recv_array(socket, flags=0, copy=True, track=False):
    """recv a numpy array"""
    md = socket.recv_json(flags=flags)
    msg = socket.recv(flags=flags, copy=copy, track=track)
    buf = memoryview(msg)
    A = numpy.frombuffer(buf, dtype=md['dtype'])
    return A.reshape(md['shape'])



