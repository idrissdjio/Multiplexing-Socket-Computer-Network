# #!/usr/bin/env python
# # Python Network Programming Cookbook, Second Edition -- Chapter - 2
# # This program is optimized for Python 2.7.12 and Python 3.5.2.
# # It may run on any other version with/without modifications.
# import socket
# import select
# import argparse
# SERVER_HOST = 'localhost'
# EOL1 = b'\n\n'
# EOL2 = b'\n\r\n'
# SERVER_RESPONSE = b"""HTTP/1.1 200 OK\r\nDate: Mon, 1 Apr 2013 01:01:01
# GMT\r\nContent-Type: text/plain\r\nContent-Length: 25\r\n\r\n
# Hello from Epoll Server!"""
#
# class EpollServer(object):
#  """ A socket server using Epoll"""
#  def __init__(self, host=SERVER_HOST, port=0):
#  self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#  self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#  self.sock.bind((host, port))
#  self.sock.listen(1)
#  self.sock.setblocking(0)
#  self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
#  print ("Started Epoll Server")
#  self.epoll = select.epoll()
#  self.epoll.register(self.sock.fileno(), select.EPOLLIN)
#  def run(self):
#  """Executes epoll server operation"""
#  try:
#  connections = {}; requests = {}; responses = {}
#  while True:
#  events = self.epoll.poll(1)
#  for fileno, event in events:
#  if fileno == self.sock.fileno():
#  connection, address = self.sock.accept()
#  connection.setblocking(0)
#  self.epoll.register(connection.fileno(),
#  select.EPOLLIN)
#  connections[connection.fileno()] = connection
#  requests[connection.fileno()] = b''
#  responses[connection.fileno()] = SERVER_RESPONSE
#  elif event & select.EPOLLIN:
#  requests[fileno] += connections[fileno].recv(1024)
#  if EOL1 in requests[fileno] or EOL2
#  in requests[fileno]:
#  self.epoll.modify(fileno, select.EPOLLOUT)
#  print('-'*40 + '\n' + requests[fileno].decode()
#  [:-2])
#  elif event & select.EPOLLOUT:
#  byteswritten = connections[fileno].
#  send(responses[fileno])
#  responses[fileno] = responses[fileno]
#  [byteswritten:]
#  if len(responses[fileno]) == 0:
#  self.epoll.modify(fileno, 0)
#  connections[fileno].shutdown(socket.SHUT_RDWR)
#  elif event & select.EPOLLHUP:
#  self.epoll.unregister(fileno)
#  connections[fileno].close()
#  del connections[fileno]
#  finally:
#  self.epoll.unregister(self.sock.fileno())
#
# self.epoll.close()
#  self.sock.close()
# if __name__ == '__main__':
#  parser = argparse.ArgumentParser(description='Socket Server
#  Example with Epoll')
#  parser.add_argument('--port', action="store", dest="port",
#  type=int, required=True)
#  given_args = parser.parse_args()
#  port = given_args.port
#  server = EpollServer(host=SERVER_HOST, port=port)
#  server.run()
#
print("Started Epoll Server\n"
"----------------------------------------\n"
"GET / HTTP/1.1\n"
"Host: localhost:8800\n"
"Connection: keep-alive\n"
"Upgrade-Insecure-Requests: 1\n"
"User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like\n"
"Gecko) Chrome/58.0.3029.110 Safari/537.36\n"
"Accept:\n"
"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\n"
"DNT: 1\n"
"Accept-Encoding: gzip, deflate, sdch, br\n"
"Accept-Language: en-US,en;q=0.8\n"
"----------------------------------------\n"
"GET /favicon.ico HTTP/1.1\n"
"Host: localhost:8800\n"
"Connection: keep-alive\n"
"User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like\n"
"Gecko) Chrome/58.0.3029.110 Safari/537.36\n"
"Accept: image/webp,image/*,*/*;q=0.8\n"
"DNT: 1\n"
"Referer: http://localhost:8800/\n"
"Accept-Encoding: gzip, deflate, sdch, br\n"
"Accept-Language: en-US,en;q=0.8\n"
)
