import socket
import hashlib
from _thread import *
import time
import logging
from datetime import datetime

## Inicialización Logging
now=datetime.now()
filename=str(now.year)+'-'+str(now.month)+'-'+str(now.day)+'-'+str(now.hour)+'-'+str(now.minute)+'-'+str(now.second)+'-logServidor.txt'
logging.basicConfig(filename=filename, level=logging.DEBUG)


# Creación socket servidor
ServerSocket=socket.socket()
# Inicialización variables
host='127.0.0.1'
port=1233
ThreadCount=0
Connections=0
PaquetesEnviados=0
Clientes=[]
EstadoClientes='Listo para recibir'

# Binding socket to host and port
try:
    ServerSocket.bind((host,port))
except socket.error as e:
    print(str(e))


# Servidor comenzando, inicializacipon conexiones esperadas y archivo a enviar
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
# Socket listo para recibir conexiones
ServerSocket.listen(5)
# Información guardada en el log
logging.info('Nombre de archivo enviado: '+Archivo)
logging.info('Tamaño de archivo enviado: '+Archivo_Tamaño+' MB')
print('Server listening....')
## Función para hallar el hash al archivo
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
## Función para enviar hash a cliente del respectivo archivo
def enviar_hash(connection,i):
    message = hash_file(Archivo)
    print(message)
    connection.send(str.encode(message))
    b=connection.recv(1024).decode('utf-8')
    if 'No' in b:
        logging.info('Transferencia no exitosa a cliente '+str(i))
    else:
        logging.info('Transferencia exitosa a cliente '+str(i))

## Función de envío archivo al cliente
def threaded_client(connection,i):
    while True:
        filename =Archivo  # In the same folder or path is this file running must the file you want to tranfser to be
        # Apertura archivo
        f = open(filename, 'rb')
        # Lectura archivo
        l = f.read(1024)
        tiempo_Inicio = datetime.now()
        while (l):
            try:
                # Envio archivo
                connection.send(l)
                # print('Sent ', repr(l))
                l = f.read(1024)
            except Exception:
                pass
        # Cierre archivo
        f.close()

        print('Done sending \n')
        # Calculo tiempo total de envío
        tiempo_Final=datetime.now()
        tiempo_Envio=tiempo_Final-tiempo_Inicio
        tiempo_Envio=tiempo_Envio.microseconds
        logging.info('Tiempo envio de archivo a cliente '+str(i)+':'+str(tiempo_Envio)+' microsegundos')
        connection.send(str.encode('Thank you for connecting'))
        time.sleep(5)
        enviar_hash(connection,i)




        connection.close()
# Conexion activa a clientes e inicio de funciones
while True:
    Client,address=ServerSocket.accept()
    print('Connected to: '+address[0]+':'+str(address[1]))
    Booleano=EstadoClientes==(Client.recv(1024).decode('utf-8'))
    if Booleano:
        Connections+=1
        Clientes.append(Client)
    else:
        Client.close()
    if Connections==NumeroConexiones:
        print('Se comienza a enviar el archivo')
        for i in range(NumeroConexiones):
            Clientes[i].send(str.encode(str(i+1)+'-'+str(NumeroConexiones)+'-'+Archivo))
            print('Enviando número de thread y conexiones totales')
            time.sleep(1)
            start_new_thread(threaded_client,(Clientes[i],i+1,))
            ThreadCount+=1
            logging.info('Cantidad de conexiones: ' + str(NumeroConexiones) + ' Número de Cliente ' + str(ThreadCount))
            print('Thread Number: '+str(ThreadCount))
        Clientes=[]
        Connections=0
        ThreadCount=0

ServerSocket.close()



