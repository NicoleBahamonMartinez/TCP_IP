import socket
import os
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

##
def threaded_client(connection):
    connection.send(str.encode('Welcome to the Servern'))
    while True:
        data = connection.recv(2048)
        filename=Archivo #In the same folder or path is this file running must the file you want to tranfser to be
        f = open(filename,'rb')
        l = f.read(1024)
        while (l):
            connection.send(l)
            print('Sent ',repr(l))
            l = f.read(1024)
            f.close()

        print('Done sending \n')
        connection.send(str.encode('Thank you for connecting'))

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



