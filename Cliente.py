# Author: Mario Valderrama
# Date: 2020

import socket
import pickle

TCP_IP='169.254.164.126'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "data2"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while 1:
    data_String = pickle.dumps([MESSAGE])
    s.send(data_String)
    data_Rec = s.recv(BUFFER_SIZE)
    data_Arr = pickle.loads(data_Rec)
    print(data_Arr)



