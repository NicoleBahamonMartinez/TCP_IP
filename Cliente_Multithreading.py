import socket
import hashlib

ClientSocket=socket.socket()
host='127.0.0.1'
port=1233


print('Waiting for connection')
try:
    ClientSocket.connect((host,port))
except socket.error as e:
    print(str(e))
##

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
        # print('data=%s', (data))
        if 'Thank you for connecting' in data.decode():
            hash_recibido=ClientSocket.recv(1024).decode()
        elif not data:
            break
        # write data to a file
        else:
            f.write(data)

f.close()
print('Successfully get the file')
print(hash_recibido)
ClientSocket.close()
print('connection closed')

def hash_file(filename):
   """"This function returns the SHA-1 hash
   of the file passed into it"""

   # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()

message = hash_file('received_file')
if hash_recibido!=message:
    print('Error, el archivo no mantiene su integridad')
else:
    print('Archivo recibido correctamente')