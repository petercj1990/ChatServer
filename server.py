import socket
import sys
from _thread import *

host = ''
port = 9020
chatbufflen = 4096
#set up the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#trys to make 
try:
	s.bind((host,port))
except socket.error as e:
	print(str(e))

s.listen(5)
print('waiting for connection \n')
# establishes connection
def threaded_client(conn):

	name = 'unknown'
	chatbuff = []
	yaboi = "Welcome to "+ name + "'s chat room\r\n"
	conn.send(str.encode( yaboi ))
#while connection is open reacts to clients commands
	stay = True;
	reply = ""
	while stay:
		# print( "\n")
		data=conn.recv(chatbufflen)
		reply=data.decode('utf-8')
		# print("|"+ reply + "|")
		# if reply.endswith('\r\n'):
		# 	reply = reply[0,-2]
		# print(reply + "\r\n")
		enc = str.encode(reply)
		
		if not data:
			break
		if reply.startswith('help'):
			# print('help' )
			reply = ""
			helpret = """Client request \"help<cr><lf>\" receives a response of a list of the commands and their syntax.\n
		Client request \"test: words<cr><lf>\"  receives a response of \"words<cr><lf>\".
		Client request \"name: <chatname><cr><lf>\" receives a response of \"OK<cr><lf>\".
		Client request \"get<cr><lf>\" receives a response of the entire contents of the chat buffer.
		Client request \"push: <stuff><cr><lf>\" receives a response of \"OK<cr><lf>\".  The result is that \"<chatname>: <stuff>\" is added as a new line to the chat buffer.
		Client request \"getrange <startline> <endline><cr><lf>\" receives a response of lines <startline> through <endline> from the chat buffer.Client request \"adios<cr><lf>\" will quit the current connection\r\n
		"""
			conn.send(str.encode(helpret[0:-3]))
		elif reply.startswith('adios'):
			# print('adios' 
			stay = False;
			conn.close()
		elif reply.startswith('test: '):
			# print("test" )
			words = reply[6:-2]
			# print("|" + words + "|")
			conn.send(str.encode(words+'\r\n'))
		elif reply.startswith('name: '):
			# print('name')
			name = reply[6:-2]
			# print("|" + name + "|")
			conn.send(str.encode('OK\r\n'))
		elif reply.startswith('time'):
			import time
			ts = time.time()
			import datetime
			st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
			conn.send(str.encode(st+'\r\n'))
		elif reply.startswith('getrange: '):
			print('getrange')
			numbers = reply.split(' ', 1)[1]
			one = int(numbers.split(' ', 1)[0])
			two = int(numbers.split(' ', 1)[1])
			# print("range 1:" + str(one) + " 2 " + str(two))
			if one < 0 or one >= len(chatbuff):
				conn.send(str.encode('Out of Range\r\n'))
			elif two < 0 or two >= len(chatbuff):
				conn.send(str.encode('Out of Range\r\n'))
			else:
				chat_ranged = ""
				for i in range(one, two):
					print('your stuff is' + i)
					chat_ranged= chat_ranged + chatbuff[i] + '\n'
				conn.send(str.encode(chat_ranged+'\r\n'))
				chat_ranged = ""

		elif reply.startswith('push: '):
			# print('push')
			import time
			ts = time.time()
			import datetime
			st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
			stuff = reply[6:-2]
			chatbuff.append(name+': '+stuff+"\t" + st)
			# print("|" + chatbuff[len(chatbuff) -1] + "|")
			conn.send(str.encode('OK\r\n'))
		elif reply.startswith('get'):
			# print('get')
			chat_ranged = ""
			for i in chatbuff:
				chat_ranged= chat_ranged + i + "\n"
			chat_ranged = chat_ranged + "\r\n"
			conn.send(str.encode(chat_ranged))
		else:
			# print("error")
			conn.send(str.encode( "Error: unrecognized command: "+reply+"\r\n"))

	#what closes the connection
	reply = ""
	conn.close()
# shows what is happening on server side
while True:
	conn, addr = s.accept()
	print('connected to: ' + addr[0] + ':' + str(addr[1]))
	start_new_thread(threaded_client,(conn,))
