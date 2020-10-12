from utility import init_sockets, send_array, recv_array

class BaseModeler:

    def __init__(self, source, destination):

        self.receiver, self.sender = init_sockets(source, destination)

    def busy_loop(self):
        while True:
            try:
                # data = self.receiver.recv()
                data = recv_array(self.receiver)
                print("Data in", self.__class__.__name__, data)
                result = self.compute(data)
                # self.sender.send(result)
                send_array(self.sender, result)
            except KeyboardInterrupt:
                print('Module {} exiting'.format(self.__class__.__name__))
                break

    def compute(self, data):
        raise NotImplementedError('This should be implemented by derived class')

