#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 2
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.
import select
import socket
import sys
import signal
import pickle
import struct
import argparse
SERVER_HOST = 'localhost'
CHAT_SERVER_NAME = 'server'
# Some utilities
def send(channel, *args):
 buffer = pickle.dumps(args)
 value = socket.htonl(len(buffer))
 size = struct.pack("L",value)
 channel.send(size)
 channel.send(buffer)
def receive(channel):
 size = struct.calcsize("L")
 size = channel.recv(size)
 try:
 size = socket.ntohl(struct.unpack("L", size)[0])
 except struct.error as e:
     return ''
 buf = ""
 while len(buf) < size:
 buf = channel.recv(size - len(buf))
 return pickle.loads(buf)[0]
class ChatServer(object):
 """ An example chat server using select """
 def __init__(self, port, backlog=5):
 self.clients = 0
 self.clientmap = {}
 self.outputs = [] # list output sockets
 self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 self.server.bind((SERVER_HOST, port))
 print ('Server listening to port: %s ...' %port)
 self.server.listen(backlog)
 # Catch keyboard interrupts
 signal.signal(signal.SIGINT, self.sighandler)
 def sighandler(self, signum, frame):
 """ Clean up client outputs"""
 # Close the server
 print ('Shutting down server...')
 # Close existing client sockets
 for output in self.outputs:
 output.close()
 self.server.close()
 def get_client_name(self, client):
 """ Return the name of the client """
 info = self.clientmap[client]
 host, name = info[0][0], info[1]
 return '@'.join((name, host))

 def run(self):
 inputs = [self.server, sys.stdin]
 self.outputs = []

running = True
 while running:
 try:
 readable, writeable, exceptional = select.
 select(inputs, self.outputs, [])
 except select.error as e:
 break
 for sock in readable:
 if sock == self.server:
 # handle the server socket
 client, address = self.server.accept()
 print ("Chat server: got connection %d from %s" %
 (client.fileno(), address))
 # Read the login name
 cname = receive(client).split('NAME: ')[1]
 # Compute client name and send back
 self.clients += 1
 send(client, 'CLIENT: ' + str(address[0]))
 inputs.append(client)
 self.clientmap[client] = (address, cname)
 # Send joining information to other clients
 msg = "\n(Connected: New client (%d) from %s)" %
 (self.clients, self.get_client_name(client))
 for output in self.outputs:
 send(output, msg)
 self.outputs.append(client)
 elif sock == sys.stdin:
 # handle standard input
 junk = sys.stdin.readline()
 running = False
 else:
 # handle all other sockets
 try:
 data = receive(sock)
 if data:
 # Send as new client's message...
 msg = '\n#[' + self.get_client_name(sock)
 + ']>>' + data
 # Send data to all except ourself
 for output in self.outputs:
 if output != sock:
 send(output, msg)
 else:
 print ("Chat server: %d hung up"
 % sock.fileno())
 self.clients -= 1

sock.close()
 inputs.remove(sock)
 self.outputs.remove(sock)
 # Sending client leaving information to others
 msg = "\n(Now hung up: Client from %s)" %
 self.get_client_name(sock)
 for output in self.outputs:
 send(output, msg)
 except socket.error as e:
 # Remove
 inputs.remove(sock)
 self.outputs.remove(sock)
 self.server.close()















