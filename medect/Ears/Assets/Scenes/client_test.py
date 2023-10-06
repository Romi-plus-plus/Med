import zmq
import sys

context = zmq.Context()
print("Connecting to server...")

socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

# socket = context.socket(zmq.REQ)
# socket.setsockopt(zmq.LINGER, 0)
# socket.connect("tcp://localhost:5555")

poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)


for i in range(10):
    if poller.poll(10*1000): 
        message = socket.recv()
        print("Received reply: ", message.decode('utf-8'))
    else:
        raise IOError("Timeout processing auth request")

    socket.send(b'1,1')
socket.close()
context.term()
sys.exit(0)
