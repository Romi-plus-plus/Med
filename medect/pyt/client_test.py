import zmq
import sys
import time

context = zmq.Context()
print("Connecting to server...")

socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)


for i in range(1000):
    if poller.poll(10*1000): 
        message = socket.recv()
        print("Received reply: ", message.decode('utf-8'))
    else:
        raise IOError("Timeout processing auth request")

    # socket.send(b'from server: %d' % i)
    message = input("Send: ")
    socket.send_string(message)

    time.sleep(0.1)

socket.close()
context.term()
sys.exit(0)
