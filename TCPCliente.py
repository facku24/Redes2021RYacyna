# Usage: python TCPCliente.py -p=nnnnn -n='000.0.0.0'
#  Con "close" cierra sesion en cliente.
#  Con "finalclose" cierra sesion en Cliente y en Servidor.
from socket import *
import argparse
from os import listdir

# Procesa argumentos.
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, help="Puerto del servidor", default=12000)
parser.add_argument("-n", "--name", help="Server Name", default='127.0.0.1')
args = parser.parse_args()
if args.port:
    print ("Conectarse al puerto: ", args.port)
    serverPort = args.port
if args.name:
    print ("Servidor: ", args.name)
    serverName = args.name


clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName,serverPort))

print ()
print ("      'close': cierra sesion del cliente.")
print (" 'finalclose': cierra sesion del cliente y servidor.")
print (" '     'list': recibe listado de archivos.")
print (" '      'get': solicita un archivo del server.")
print ("   'metadata': solicita metadata de un archivo jpeg/jpg.")
print ()


#nombrecliente = input('Cual es su nombre Cliente ? ') 

while 1:
	parametro = '.'
	sentence  = input('Ingrese comando :')
	clientSocket.send( sentence.encode() )
	
	if sentence == 'get':
		parametro = input('Ingrese nombre de archivo a recibir:')
		clientSocket.send(parametro.encode())		
		print()
		input('Pulse una tecla para continuar ... ')

	if sentence=='close' or sentence=='finalclose': 
		break
	
	if sentence == 'list':
		parametro = input('Pulse una tecla para continuar ... ')

	if sentence == 'metadata':
		parametro = input('Ingrese nombre de archivo "jpeg/jpg" :')
		clientSocket.send(parametro.encode())		
		print()
		input('Pulse una tecla para continuar ... ')
		
	modifiedSentence = clientSocket.recv(1024)
	print('')
	print('Desde Server: ' + modifiedSentence.decode())

clientSocket.close()


