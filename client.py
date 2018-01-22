import serial
from time import strftime, localtime

# open serial port (9600 baud, 8N1)
ser_conn = serial.Serial("/dev/ttyUSB0") # test port on Mac.

while True:
	ser_out = input("Please input serial command (A/B): ")

	ser_out = ser_out.encode()


	if ser_out == b"A" or ser_out == b"B":
		ser_conn.write(ser_out)
		ser_in = ser_conn.readline()
		print(ser_in)
	else:
		print("Not a valid command!")
