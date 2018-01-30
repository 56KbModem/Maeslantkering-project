# making the server
import socket
import requests

HOST = '192.168.42.100'
PORT = 10000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
        s.bind((HOST, PORT)) # Bind socket to localhost:
        print("socket bound to {}:{}".format(HOST, str(PORT)))
except socket.error as e:
        print('Something went wrong while trying to bind port: {}'.format(str(e)))

s.listen(5)
print("listen call completed")

# Handling client connection
def client_connection(connect):
    status = "open"
    while True:
        data = connect.recv(1024)
        data = data.decode()
        data = data.strip("\r\n").split(" ")

        waterhogte = data[1]
        plaats = data[0]

        ### hier zijn de limits bereikt :
        if plaats=="RD" and int(waterhogte)>=300 and status == "open" :
            reply = "A"   # A is close
            status = "close"
            message = "De kering gaat dicht. Waterhogte is: "+waterhogte
        elif plaats=="DD" and int(waterhogte)>=290 and status == "open" :
            reply = "A"   # A is close
            status = "close"
            message = "De kering gaat dicht. Waterhogte is: "+waterhogte
        ### hier zijn de limits niet bereikt :
        elif plaats=="RD" and int(waterhogte)<300 and status == "close" :
            reply = "B" #B is open
            status = "open"
            message = "De kering gaat open. Waterhogte is: "+waterhogte
        elif plaats=="DD" and int(waterhogte)<290 and status == "close" :
            reply = "B" #B is open
            status = "open"
            message = "De kering gaat open. Waterhogte is: "+waterhogte
        else:
            continue

        connect.sendall(str.encode(reply))
        ### send the update to telegram
        tele_protocol = "https://api.telegram.org/bot520998188:AAEOroYyol_A6A2yIFuzDrgMUZTlX0Y-Ofc/sendMessage?chat_id=409845558&text="
        requests.get(tele_protocol+message)

    connect.close()

while True:
        connect, address = s.accept()
        print('connect from: {0}:{1}'.format(address[0], str(address[1])))

        client_connection(connect)
