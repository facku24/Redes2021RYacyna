from socket import *

serverName = '127.0.0.1'
serverPort = 12000

# AF_INET establece como protocolo de red a IP
# SOCK_STREAM establece como protocolo de transporte a TCP

def create_socket(addr, port):
	serverSocket = socket(AF_INET, SOCK_STREAM)
	serverSocket.bind((serverName,serverPort))
	# ligarlo
	
	serverSocket.listen(1)
	return serverSocket
def main():
        serverSocket= create_socket(serverName, serverPort)	
        print('El server esta listo para recibir ... ')

        while 1:
                connectionSocket, addr = serverSocket.accept()
                sentence = connectionSocket.recv(1024)
				#print (sentence.decode())
                capitalizedSentence = sentence.decode().upper()
                connectionSocket.send(capitalizedSentence.encode())
                connectionSocket.close()



if __name__ == '__main__':
        main()
        

