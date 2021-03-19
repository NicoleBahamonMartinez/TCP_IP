import socket

ClientSocket=socket.socket()
host='127.0.0.1'
port=1233


print('Waiting for connection')
try:
    ClientSocket.connect((host,port))
except socket.error as e:
    print(str(e))

# while True:
#     estado='Listo para recibir'
#     ClientSocket.send(str.encode(estado))
#     with open('received_file_nuevo', 'wb') as f:
#         print('file opened')
#         while True:
#             print('receiving data...')
#             data = ClientSocket.recv(1024)
#             print(data)
#             print('data=%s', (data))
#             if not data:
#                 print('No hay data')
#                 break
#             f.write(data)
#
#     f.close()
# ClientSocket.close()

with open('received_file', 'wb') as f:
    print('file opened')
    while True:
        print('receiving data...')
        data = ClientSocket.recv(1024)
        print('data=%s', (data))
        if not data:
            break
        # write data to a file
        f.write(data)

f.close()
print('Successfully get the file')
ClientSocket.close()
print('connection closed')