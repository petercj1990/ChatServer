from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer
from urlparse import urlparse, parse_qs
from os import curdir, sep
import re
import cgi
# import asyncore import dispacher
import socket
import sys
# from _thread import *
PUBLIC_RESOURCE_PREFIX = '/'
PUBLIC_DIRECTORY = './'


PORT_NUMBER = 8081

#This class will handles any incoming request from
#the browser 
class myHandler(SimpleHTTPRequestHandler):
	def translate_path(self, path):
	    if self.path.startswith(PUBLIC_RESOURCE_PREFIX):
	        if self.path == PUBLIC_RESOURCE_PREFIX or self.path == PUBLIC_RESOURCE_PREFIX + '/':
	            return PUBLIC_DIRECTORY + '/index.html'
	        else:
	            return PUBLIC_DIRECTORY + path[len(PUBLIC_RESOURCE_PREFIX):]
	    else:
	    	return SimpleHTTPServer.SimpleHTTPRequestHandler.translate_path(self, path)
	#Handler for the GET requests
	def do_GET(self):
		if self.path=="/chat":
			self.path="/public/chat.html"
		if self.path=="/chathistory":
			self.path="/public/chathistory.txt"
			print "im here"

		if re.search("^/SEND",self.path):
			values = parse_qs(urlparse(self.path).query)
			username = values['username'][0]
			message = values['message'][0]
			if username == "":
				username = "Guest"
			if message == "":
				message = "no message man"
            #sep separator, accounts for backslash or forward slash depending on os
			fHandle = open(curdir + sep + "public/chathistory.txt", "a")  
			fHandle.write("<span>" + username + ":</span>" + message + "<br>\n")
			fHandle.close()
			self.path = "./public/chat.html"

		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".txt"):
				mimetype='text/plain'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True
			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	#Handler for the POST requests
	def do_POST(self):
		if self.path=="/send":
			form = cgi.FieldStorage(
				fp=self.rfile, 
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
		                 'CONTENT_TYPE':self.headers['Content-Type'],
			})

			print "Your name is: %s" % form["your_name"].value
			self.send_response(200)
			self.end_headers()
			self.wfile.write("Thanks %s !" % form["your_name"].value)
			return			
			
			
try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = SocketServer.TCPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
	

