import sys
import socket
import time
from thread import *
from random import randint

bufferSize = 1024
host = '192.168.1.9'
port = 5500
numOfClients = 5
numOfActiveConnections = 0

def clientThread(conn,s):
	global numOfActiveConnections
	try:
		#conn.send("Welcome to the server. Type something and hit ENTER\n")
                FLAG_RESPONSE = True
		while True:
			data = conn.recv(bufferSize)
			if not data: 
				break
			print data
                        if FLAG_RESPONSE:
				if randint(0,1):
					reply = "VALVE NO%c" % '\a'
				else:
					reply = "VALVE NC%c" % '\a'
				print reply
				conn.sendall(reply)
				FLAG_RESPONSE = False
			if data == 'EXIT':
				conn.sendall("The connection is terminated.")
				break
		conn.close()
		numOfActiveConnections-= 1

		print "Number of Active connections: " + str(numOfActiveConnections)
	except:
		numOfActiveConnections-= 1
		print "An error occured and the client is disconnected"
		exit()


def startService():
	'''
	This function binds a socket to a specific port and
	is waiting for incoming connections. Can serve up to 
	numOfClients clients.
	'''
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
		try:
			#wait for a connection - blocking call
			conn, addr = s.accept()
		except socket.error as msg:
			print "An error occured: " + str(msg)
			s.close()
			sys.exit()

		print 'Connected with ' + str(addr[0]) + ':' + str(addr[1])

		start_new_thread(clientThread, (conn,s))
		global numOfActiveConnections
		numOfActiveConnections += 1
		print "Number of Active connections: " + str(numOfActiveConnections)
		

	
