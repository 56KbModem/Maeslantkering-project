import socket
import sys

#Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Bind socket to port
server_address = ('localhost', 10000)
print (sys.stdout, 'starting up on %s port %s' % server_address)
sock.bind(server_address)
#listen for incoming connections
sock.listen(1)

while True:
    print (sys.stdout, 'Waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print (sys.stdout, 'client connected:', client_address)
        while True:
            data = connection.recv(16)
            print (sys.stdout, 'received "%s"' % data)
            if data:
                connection.sendall(data)
            else:
                break
    finally:
        connection.close()