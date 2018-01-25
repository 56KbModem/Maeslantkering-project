import serial
import socket
import os
from time import strftime, localtime

server1 = ("192.168.42.100", 10000)
server2 = ("192.168.42.200", 10000)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # tcp socket

# open serial port (9600 baud, 8N1)
ser_conn = serial.Serial("/dev/ttyUSB0") 


while True:
	ser_in = ser_conn.readline()
	ser_out = connect_it(ser_in)

	if ser_out == b"A" or ser_out == b"B": # close or open command
		ser_conn.write(ser_out)
		connect_it(ser_conn.readline())
	elif ser_out == b"C": # nothing critical
		continue
	else:
		log_event("Unkown message received: {}".format(ser_out.decode()))

# send message to server
# if server1 fails, it will
# try to connect to server2
def connect_it(serial_message):
	try:
		s.connect(server1)
		log_event("connection established to server 1")
		s.send(serial_message)
		ser_out = s.recv(512)

		return ser_out

	except ConnectionRefusedError:
		log_event("trying failover server2, server 1 doesn't respond")
		s.connect(server2)
		s.send(serial_message)
		ser_out = s.recv(512)

		return ser_out

# check if logfile exists, else create it
def write_or_append():
	if os.path.exists('/home/pi/client.log') == True:
		file_mode = 'a'
	else:
		file_mode = 'w'
	return file_mode

# log server events
def log_event(message):
	file_mode = write_or_append()
	log_file = open('alarm.log', file_mode)
	time_stamp = strftime("%Y-%m-%d %H:%M:%S", localtime())

	event = time_stamp + ': ' + message + '\n'

	log_file.write(event)
