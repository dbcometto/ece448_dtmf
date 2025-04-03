# This is the python script that will convert a linear coordinate published via ZMQ Push to the corresponding DTMF character
# Written by Ben Cometto, 18 Feb 2025

import zmq
import struct
import sys
import time


current_time = 0
last_time = 0
period_ms = 100

# variables
socket_loc = "tcp://localhost:4444"


#  Set up socket to talk to GNU Radio
context = zmq.Context()
pull_socket = context.socket(zmq.PULL)
#pull_socket.setsockopt(zmq.CONFLATE, 1)
pull_socket.connect(socket_loc)

print(f" I am setup and waiting for messages on {socket_loc}")


current_data = b""
my_int = 99
state = 0 # 0 means waiting for data, 1 means received data waiting for break

decodeTable = {0:"1",1:"2",2:"3",3:"A",
               4:"4",5:"5",6:"6",7:"B",
               8:"7",9:"8",10:"9",11:"C",
               12:"*",13:"0",14:"#",15:"D"}

# Main Processing Loop
while True: 

    # get new data every once in a while
    current_time = time.time()*1000
    if (current_time-last_time) > period_ms:
        # Get new data
        try:
            current_data += pull_socket.recv(flags=zmq.NOBLOCK) # concactenate new data onto old data
        except:
            pass   

        last_time = current_time 

    # If there is enough data, get a new integer    
    while len(current_data) >= 1: 
        # pull int out of byte data
        my_int = int.from_bytes(current_data[:4], byteorder="little") #int.from_bytes(current_data[0]) 
        current_data = current_data[4:] # delete data off of the front of the queue

        # current state and next state logic

        if state == 0:
            #print("state 0")
            if my_int != 99:
                print(decodeTable[my_int], end="")
                sys.stdout.flush()
                state = 1

        elif state == 1:
            #print("state 1")
            if my_int == 99:
                state = 0
        