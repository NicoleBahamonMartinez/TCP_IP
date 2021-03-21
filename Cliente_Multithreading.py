import socket
import hashlib
import os
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
## Fúncion para hacer hashing del archivo
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
## Estado actual del cliente
if nombre_Archivo=='':
    Estado='Listo para recibir'
    ClientSocket.send(str.encode(Estado))
else:
    ClientSocket.send(str.encode('Recibiendo Archivo'))
## Recibimiento de datos del servidor
datos_iniciales = ClientSocket.recv(1024)
datos_iniciales=datos_iniciales.decode()
datos_iniciales=str(datos_iniciales)
datos_iniciales=datos_iniciales.split('-')

## Creación de path donde se guarda el archivo
if not os.path.exists('ArchivosRecibidos'):

    os.makedirs('ArchivosRecibidos')
nombre_Archivo='ArchivosRecibidos/Cliente'+str(datos_iniciales[0])+'-Prueba-'+str(datos_iniciales[1])+'.txt'

print(nombre_Archivo)
# Logging
logging.info('Nombre de archivo recibido :'+str(datos_iniciales[2]))
logging.info('Soy el cliente '+str(datos_iniciales[0]+' de '+str(datos_iniciales[1])+' conexiones'))

## Escritura de paquetes recibidos hacia archivo
with open(nombre_Archivo, 'wb') as f:
    print('file opened')
    tiempo_Inicio = datetime.now()
    while True:
        print('receiving data...')
        data = ClientSocket.recv(1024)
        # print('data=%s', (data))
        if 'Thank you for connecting' in data.decode():
            hash_recibido=ClientSocket.recv(1024).decode()
            print(hash_recibido)
            print('Recibe el hash')
            print('Closing file')
            tiempo_Final = datetime.now()
            break
        # write data to a file
        else:
            f.write(data)

f.close()
print('Successfully get the file')
tamanio_Archivo=os.stat(nombre_Archivo).st_size
logging.info('Tamaño de archivo recibido: '+str(tamanio_Archivo)+' bytes')
tiempoTotal=(tiempo_Final-tiempo_Inicio).microseconds
logging.info('Tiempo recepción de archivo  :' + str(tiempoTotal) + ' microsegundos')
##
NumPaquetesRecibidos=tamanio_Archivo/1024+3
NumBytesRecibidos=tamanio_Archivo+(1024*3)
logging.info('Numero Paquetes Recibidos: '+str(NumPaquetesRecibidos))
logging.info('Numero Bytes Recibidos: '+str(NumBytesRecibidos))
## Hashing del archivo
print('Comienza el hashing')
message = hash_file(nombre_Archivo)
print('Termina el hashing')
if hash_recibido!=message:
    ClientSocket.send(str.encode('No se mantiene la integridad'))
    print('Error, el archivo no mantiene su integridad')
    logging.info('Archivo recibido no exitosamente')
else:
    ClientSocket.send(str.encode('Se mantiene la integridad'))
    print('Archivo recibido correctamente')
    logging.info('Archivo recibido exitosamente')
ClientSocket.close()
print('connection closed')

