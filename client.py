from socket import *

HOST="169.254.215.140"
#HOST = gethostbyname(gethostname())
PORT = 27777
ADDR = (HOST, PORT)
BUFSIZ = 1024

tcpCliSocket = socket(AF_INET, SOCK_STREAM)
#tcpCliSocket.bind(('10.100.24.2',27777))
tcpCliSocket.connect(ADDR)
try:
	while True:
		data = input('> ')
		if not data:
			break
		tcpCliSocket.send(data.encode('utf8'))
		
		data = tcpCliSocket.recv(BUFSIZ)
		if not data:
			break
		print(data.decode('utf8'))
except KeyboardInterrupt:
	tcpCliSocket.close()