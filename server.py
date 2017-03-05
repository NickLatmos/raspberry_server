import socket
import sys
from thread import *
import clientHandler 

host = '192.168.1.20'
port = 5500
numOfClients = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
	s.bind((host,port))
except socket.error as msg:
	print 'Bind failed. Error code : ' + str(msg[0]) + "Message : " + str(msg[1])
	sys.exit()

print 'Socket bind complete'


s.listen(numOfClients)
print 'Socket now listening for maximum ' + str(numOfClients) + " clients"

while True:
	#wait for a connection - blocking call
	conn, addr = s.accept()
	print 'Connected with ' + str(addr[0]) + ':' + str(addr[1])

	start_new_thread(clientHandler.clientThread, (conn,))

s.close()
