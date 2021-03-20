import socket
import os
import hashlib
from _thread import *
import time
import logging
from datetime import datetime

now=datetime.now()
filename=str(now.year)+'-'+str(now.month)+'-'+str(now.day)+'-'+str(now.hour)+'-'+str(now.minute)+'-'+str(now.second)+'-logServidor.txt'
logging.basicConfig(filename=filename, level=logging.DEBUG)



ServerSocket=socket.socket()
host='127.0.0.1'
port=1233
ThreadCount=0
Connections=0
Clientes=[]
EstadoClientes='Listo para recibir'

try:
    ServerSocket.bind((host,port))
except socket.error as e:
    print(str(e))
##
print('Waiting for connection...')
NumeroConexiones=input('A cuantos clientes quiere enviar el archivo ?')
NumeroConexiones=int(NumeroConexiones)
Archivo_Tamaño=input('Que archivo quiere mandar? (Opciones posibles 100-250)')
if Archivo_Tamaño=='100':
    Archivo='Archivos/Archivo100.txt'
elif Archivo_Tamaño=='250':
    Archivo='Archivos/Archivo250.txt'
else:
    Archivo='Archivos/Archivo100'
    Archivo_Tamaño=100
    print('No se reconoce el archivo, se maneja el archivo de 100MB')
ServerSocket.listen(5)
logging.debug('Nombre de archivo enviado'+Archivo)
logging.debug('Tamaño de archivo enviado'+Archivo_Tamaño+'MB')
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
def enviar_hash(connection):
    message = hash_file(Archivo)
    print(message)
    connection.send(str.encode(message))

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
        time.sleep(5)
        enviar_hash(connection)



        connection.close()

while True:
    Client,address=ServerSocket.accept()
    print('Connected to: '+address[0]+':'+str(address[1]))
    Booleano=EstadoClientes==(Client.recv(2048).decode('utf-8'))
    if Booleano:
        Connections+=1
        Clientes.append(Client)
    else:
        Client.close()
    if Connections==NumeroConexiones:
        print('Se comienza a enviar el archivo')
        for i in range(NumeroConexiones):
            Clientes[i].send(str.encode(str(i+1)+'-'+str(NumeroConexiones)))
            print('Enviando número de thread y conexiones totales')
            time.sleep(1)
            start_new_thread(threaded_client,(Clientes[i],))
            ThreadCount+=1
            print('Thread Number: '+str(ThreadCount))
        Clientes=[]
        ThreadCount=0
        Connections=0

ServerSocket.close()



