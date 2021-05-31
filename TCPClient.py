from socket import *

serverName = '127.0.0.1'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName,serverPort))

while 1:
	sentence = input('Ingrese mensaje :')
	print ('Ingreso :', sentence)
	if sentence=='SALIR': 
		break
	clientSocket.send(sentence.encode())
	modifiedSentence = clientSocket.recv(1024)
	print('Desde Server: ' + modifiedSentence.decode())

clientSocket.close()