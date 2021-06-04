# Uso: python TCPServer.py -p=nnnnn -n='000.0.0.0'
# Requiere : pip install exifread

from os import listdir
from os.path import isfile, join
from socket import *
import sqlite3
import time
import argparse
import os
import datetime
import exifread
				
# Procesa argumentos.
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, help="Puerto del servidor", default=12000)
parser.add_argument("-n", "--name", help="Server Name", default='127.0.0.1')
args = parser.parse_args()
if args.port:
    #print ("Conectarse al puerto: ", args.port)
    serverPort = args.port
if args.name:
    #print ("Servidor: ", args.name)
    serverName = args.name
	

# Conecta/crea BD
con = sqlite3.connect('server.db')
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS server ( id INTEGER PRIMARY KEY, fecha datetime, mensaje text, cliente text)") 

print ('Iniciando en ',serverPort,' ',serverName)

# AF_INET establece como protocolo de red a IP
# SOCK_STREAM establece como protocolo de transporte a TCP

def ls(ruta = '.'):
    return [arch for arch in listdir(ruta) if isfile(join(ruta, arch))]

def create_socket(addr, port):
	serverSocket = socket(AF_INET, SOCK_STREAM)
	serverSocket.bind((serverName,serverPort))
	# ligarlo
	
	serverSocket.listen(1)
	return serverSocket

def main():
	serverSocket= create_socket(serverName, serverPort)
	while 1:
		print ()
		print('El server está listo para recibir ... ')
		connectionSocket, addr = serverSocket.accept()
		while 1:
			sentence = connectionSocket.recv(1024)
			
			capitalizedSentence = sentence.decode().upper()
			connectionSocket.send( capitalizedSentence.encode() )
			print ('')
			print ('Se recibió del cliente:', capitalizedSentence)
			cur.execute("INSERT INTO server ( fecha, mensaje, cliente)  VALUES (?,?,?)", ( datetime.date.today(), capitalizedSentence,serverName))
						
			if capitalizedSentence == 'CLOSE' or capitalizedSentence == 'FINALCLOSE':
				connectionSocket.close()
				break
				
			if capitalizedSentence == 'LIST':	
				directorio = os.getcwd()  
				lista =  os.listdir(directorio)
				print ()
				for i in lista:
					#print ('Enviando ',i)
					archivo = '\n'+'Archivo '+i
					connectionSocket.send( archivo.encode() )

				final = '\n'+'...'
				connectionSocket.send( final.encode() )
				print ('')
			
			if capitalizedSentence == 'GET':				
				fichero = connectionSocket.recv(1024)
				fichero = fichero.decode()
				print ('Solicita el archivo :', fichero )

				if os.path.isfile(fichero):
						connectionSocket.send('\n EXISTE archivo ...\n\n'.encode())
						# Abrimos el archivo que queremos enviar
						with open(fichero, 'rb') as f:
							bytesToSend = f.read(1024)
							connectionSocket.send(bytesToSend)
							# En caso de que no nos lleguen los 1024 para enviar el mensaje:
							while bytesToSend:
								bytesToSend = f.read(1024)
								connectionSocket.send(bytesToSend)
				else:
					print(' No existe el archivo solicitado ! ')

				
			if capitalizedSentence == 'METADATA':				
				imagen = connectionSocket.recv(1024)
				imagen = imagen.decode()
				if os.path.isfile(imagen):
					imagen = open( imagen, 'rb')
					valores_exif = exifread.process_file(imagen)

					head = '\n\n Archivo procesado correctamente ! \n'
					connectionSocket.send( head.encode() )

					for tag in valores_exif.keys():
						meta = '\n'+str(tag) + " : " +str(valores_exif[tag])
						connectionSocket.send( meta.encode() )
					headend = '\n Fin de Metadata. \n'
					connectionSocket.send( headend.encode() )						

				else:
					connectionSocket.send( '\n\n No existe el archivo solicitado !!! \n'.encode() )
		
		
		if capitalizedSentence == 'FINALCLOSE':
			connectionSocket.close()
			break

	
	for row in cur.execute('SELECT * FROM server'):
		print(row)
 
	#Cerramos la conexion a la bd.
	#cur.commit()
	cur.close()


	
if __name__ == '__main__':
        main()
        

