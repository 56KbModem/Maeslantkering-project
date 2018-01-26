import serial
import socket
import os
from time import strftime, localtime

server1 = ("192.168.42.7", 10000)
server2 = ("192.168.42.200", 10000)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # tcp socket


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
	log_file = open('client.log', file_mode)
	time_stamp = strftime("%Y-%m-%d %H:%M:%S", localtime())

	event = time_stamp + ': ' + message + '\n'

	log_file.write(event)

ser_conn = serial.Serial("/dev/ttyUSB0")
s.connect(server1)

while True:
	# get serial data and send to server
	ser_in = ser_conn.readline()
	s.sendall(ser_in)

	# set timeout to receive command (2 seconds)
	s.settimeout(1.5)

	# get command from server
	# if it takes too long, just continue
	try:
		data = s.recv(512)
	except socket.timeout:
		continue

	print(data)

	if data == b"A\n": # close command
		ser_conn.write(b"A")
		log_event("kering gaat dicht")
	elif data == b"B\n": # open command
		ser_conn.write(b"B")
		log_event("kering gaat open")
	else:
		log_event("Unkown message received: {}".format(data.decode()))
		continue
