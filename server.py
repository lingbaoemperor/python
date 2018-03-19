from socket import *
from time import ctime 

BUFSIZ = 1024 
tcpSerSock = socket(AF_INET, SOCK_STREAM)
#HOST = gethostbyname(gethostname())
HOST="169.254.215.140"
PORT = 27777
ADDR = (HOST, PORT)
print("myaddr:%s:%s" % (HOST,PORT))

tcpSerSock.bind(ADDR)
 
tcpSerSock.listen(5)


while True:
	print("waiting for connection...")

	tcpCliSock, addr = tcpSerSock.accept()
	print("peer address is:",addr)

	while True:
		data = tcpCliSock.recv(BUFSIZ).decode('utf8')
		if not data:
			break
		#tcpCliSock.send(('[%s] %s' % (ctime(), data)).encode('utf8'))
		tcpCliSock.send(data.encode('utf8'))
	tcpCliSock.close()
tcpSerSock.close()