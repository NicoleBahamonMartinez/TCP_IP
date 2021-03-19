# Author: Mario Valderrama
# Date: 2020

import socket
import numpy as np
import pickle

TCP_IP='169.254.164.126'
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Normally 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
connnum = 50
for conncount in range(connnum):
    print('Waiting for connection...')
    conn, addr = s.accept()
    print('Connection address:', addr)
    while 1:
        msg_rec_sock = conn.recv(BUFFER_SIZE)
        if not msg_rec_sock:
            break
        msg_rec = pickle.loads(msg_rec_sock)
        msg_rec = msg_rec[0]
        # print('Received msg:', msg_rec)
        if msg_rec == "data1":
            print('Data required - msg: ', msg_rec)
            val = np.random.randint(40, 210)
            msg_str = "{:d}".format(int(val))
            msg_str_sock = pickle.dumps([msg_str])
            conn.send(msg_str_sock)
        if msg_rec == "data2":
            print('Data required - msg: ', msg_rec)
            val = np.random.randint(5, 41)
            msg_str = "{:d}".format(int(val))
            msg_str_sock = pickle.dumps([msg_str])
            conn.send(msg_str_sock)
        if msg_rec == "data3":
            print('Data required - msg: ', msg_rec)
            val = np.random.randint(78, 100)
            msg_str = "{:d}".format(int(val))
            msg_str_sock = pickle.dumps([msg_str])
            conn.send(msg_str_sock)

    conn.close()

