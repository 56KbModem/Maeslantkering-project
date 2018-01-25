import serial
import socket
from time import strftime, localtime

server1 = ("192.168.42.100", 10000)
server2 = ("192.168.42.200", 10000)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # tcp socket

# open serial port (9600 baud, 8N1)
ser_conn = serial.Serial("/dev/ttyUSB0") 

while True:
	ser_in = ser_conn.readline()
	ser_out = connect_it(ser_in)

	if ser_out == b"A" or ser_out == b"B";
		ser_conn.write(ser_out)
		connect_it(ser_conn.readline())
	else:
		write_log("Unkown message received: {}".format(str(ser_out)))

# send message to server
def connect_it(serial_message):
	try:
		s.connect(server1)
		write_log("connection established to server 1")
		s.send(serial_message)
		ser_out = s.recv(512)

		return ser_out

	except ConnectionRefusedError:
		write_log("trying failover server2, server 1 doesn't respond")
		s.connect(server2)
		s.send(serial_message)
		ser_out = s.recv(512)

		return ser_out
