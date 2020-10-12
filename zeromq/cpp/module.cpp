#include <zmq.hpp>
#include <iostream>
#include <string>

int main (int argc, char *argv[])
{

    std::string source, destination;
    // Should check number of arguments...
    source = argv[1];
    destination = argv[2];

    zmq::context_t context(1);
    
    //  Socket to receive messages on
    zmq::socket_t receiver(context, ZMQ_PULL);
    receiver.connect(source);

    //  Socket to send messages to
    zmq::socket_t sender(context, ZMQ_PUSH);
    sender.connect(destination);

    while (1) {
        zmq::message_t message;

	receiver.recv(&message);

        std::string sdata(static_cast<char*>(message.data()), message.size());

        std::cout << sdata << std::endl;
        
	//  Send stuff to sink
	zmq::message_t reply (5);
        memcpy (reply.data (), "World", 5);
        sender.send (reply);

    }
    //  Finished
    return 0;
}
