# making the server
import socket
import requests

HOST = '192.168.42.100'
PORT = 10000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
        s.bind((HOST, PORT)) # Bind socket to localhost:
except socket.error as e:
        print('Something went wrong while trying to bind port: {}'.format(str(e)))

s.listen(5)

# Handling client connection
def client_connection(connect):
    status = "open"
    while True:
        data = connect.recv(1024)
        data = data.decode()
        data = data.strip("\r\n").split(" ")

        ### hier zijn de limits bereikt :
        if data[0]=="RD" and int(data[1])>=300 and status == "open" :
            reply = "A"   # A is close
            status = "close"

        elif data[0]=="DD" and int(data[1])>=290 and status == "open" :
            reply = "A"   # A is close
            status = "close"
        ### hier zijn de limits niet bereikt :
        elif data[0]=="RD" and int(data[1])<300 and status == "close" :
            reply = "B" #B is open
            status = "open"
        elif data[0]=="DD" and int(data[1])<290 and status == "close" :
            reply = "B" #B is open
            status = "open"
        else:
            continue

        connect.sendall(str.encode(reply))
        ### send the update to telegram
        tele_protocol = "https://api.telegram.org/bot520998188:AAEOroYyol_A6A2yIFuzDrgMUZTlX0Y-Ofc/sendMessage?chat_id=409845558&text="
        if reply == "A":
            message = "the doors are closing"
        if reply == "B":
            message = "the doors are opening"
        requests.get(tele_protocol+message)


    connect.close()

client_connection(connect)
