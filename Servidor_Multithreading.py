import socket
import os
import hashlib
from _thread import *



ServerSocket=socket.socket()
host='127.0.0.1'
port=1233
ThreadCount=0
Connections=0
Clientes=[]

try:
    ServerSocket.bind((host,port))
except socket.error as e:
    print(str(e))
##
print('Waiting for connection...')
NumeroConexiones=input('A cuantos clientes quiere enviar el archivo ?')
NumeroConexiones=int(NumeroConexiones)
Archivo=input('Que archivo quiere mandar? (Opciones posibles 100-250)')
if Archivo=='100':
    Archivo='Archivos/Archivo100'
elif Archivo=='250':
    Archivo='Archivos/Archivo250'
else:
    Archivo='Archivos/Archivo100'
    print('No se reconoce el archivo, se maneja el archivo de 100MB')
ServerSocket.listen(5)
print('Server listening....')
##
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

message = hash_file(Archivo)
print(message)
##
def threaded_client(connection):
    while True:
        filename =Archivo  # In the same folder or path is this file running must the file you want to tranfser to be
        f = open(filename, 'rb')
        l = f.read(1024)
        while (l):
            try:
                connection.send(l)
                # print('Sent ', repr(l))
                l = f.read(1024)
            except Exception:
                pass
        f.close()

        print('Done sending \n')
        connection.send(str.encode('Thank you for connecting'))
        connection.send(str.encode(message))
        connection.close()

while True:
    Client,address=ServerSocket.accept()
    print('Connected to: '+address[0]+':'+str(address[1]))
    Clientes.append(Client)
    Connections+=1
    if Connections==NumeroConexiones:
        print('Se comienza a enviar el archivo')
        for i in range(NumeroConexiones):
            start_new_thread(threaded_client,(Clientes[i],))
            ThreadCount+=1
            print('Thread Number: '+str(ThreadCount))
ServerSocket.close()



