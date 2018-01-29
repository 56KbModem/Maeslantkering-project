import serial
import socket
import os
from time import strftime, localtime

server1 = ("127.0.0.1", 10000)
server2 = ("127.0.0.1", 11000)

#ser_conn = serial.Serial("/dev/ttyUSB0") # serial interface


# check if logfile exists, else create it
def write_or_append():
	if os.path.exists('/Users/nick/client.log') == True:
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

# try to make connection
# if server is down, switch connection
def make_connection(last_connected):
	if last_connected == server1[1]:
		last_connected = server2[1]
		s.connect(server2)
	elif last_connected == server2[1]:
		last_connected = server1[1]
		s.connect(server1)

	return last_connected


# handle connection with server
def handle_connection():
	while True:
		# get serial data and send to server
		#ser_in = ser_conn.readline()
		test_mess = input("Enter data for server: ")
		s.sendall(test_mess.encode())

		# set timeout to receive command (1 second)
		s.settimeout(1)

		# get command from server
		# if it takes too long, just continue
		try:
			data = s.recv(512)
		except socket.timeout:
			continue

		# send commands from server to plc
		if data == b"A\n": # close command
			#ser_conn.write(b"A")
			log_event("kering gaat dicht")
		elif data == b"B\n": # open command
			#ser_conn.write(b"B")
			log_event("kering gaat open")
		elif data == b"C\n": # change measuring place
			#ser_conn.write(b"C")
			log_event("Wissel van meetpunt")
		elif not data: # disconnect from server
			log_event("No data received, {} disconnected!".format(last_connected))
			break
		else:
			log_event("Unkown message received: {}".format(data.decode()))
			continue

###  Main  ###
last_connected = server2[1]
while True:
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		last_connected = make_connection(last_connected)
		handle_connection()
		s.close()
	except ConnectionRefusedError as e:
		log_event("Connection refused to {}".format(server1[0]))
		last_connected = make_connection(last_connected)
