import socket
import hashlib
import os
import time
import logging
from datetime import datetime

now=datetime.now()


filename=str(now.year)+'-'+str(now.month)+'-'+str(now.day)+'-'+str(now.hour)+'-'+str(now.minute)+'-'+str(now.second)+'-logCliente.txt'
logging.basicConfig(filename=filename, level=logging.DEBUG)

ClientSocket=socket.socket()
host='127.0.0.1'
port=1233
nombre_Archivo=''

print('Waiting for connection')
try:
    ClientSocket.connect((host,port))
except socket.error as e:
    print(str(e))
##
if nombre_Archivo=='':
    Estado='Listo para recibir'
    ClientSocket.send(str.encode(Estado))
else:
    ClientSocket.send(str.encode('Recibiendo Archivo'))


datos_iniciales = ClientSocket.recv(1024)
datos_iniciales=datos_iniciales.decode()
datos_iniciales=str(datos_iniciales)
datos_iniciales=datos_iniciales.split('-')

if not os.path.exists('ArchivosRecibidos'):

    os.makedirs('ArchivosRecibidos')
nombre_Archivo='ArchivosRecibidos/Cliente'+str(datos_iniciales[0])+'-Prueba-'+str(datos_iniciales[1])+'.txt'

print(nombre_Archivo)


with open(nombre_Archivo, 'wb') as f:
    print('file opened')
    while True:
        print('receiving data...')
        data = ClientSocket.recv(1024)
        # print('data=%s', (data))
        if 'Thank you for connecting' in data.decode():
            hash_recibido=ClientSocket.recv(1024).decode()
        elif not data:
            print('Closing file')
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
print('Comienza el hashing')
message = hash_file(nombre_Archivo)
print('Termina el hashing')
if hash_recibido!=message:
    print('Error, el archivo no mantiene su integridad')
else:
    print('Archivo recibido correctamente')