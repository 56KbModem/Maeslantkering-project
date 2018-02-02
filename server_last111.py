# making the server
import socket
import requests
import telegram
import time

HOST = '127.0.0.1'
PORT = 10000

bot = telegram.Bot(token= '450025897:AAENI8aZHtNBBthXaSWKQrKiQuIhVGcR7IA')
chat_id = bot.get_updates()[-1].message.chat_id
last_message_id_lijst = bot.get_updates()[-1].message.message_id

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
        if "OPEN" in data:
            status = "close"
        elif "CLOSE" in data:
            status = "close"
        else:
            data = data.strip("\r\n").split(" ")

        waterhogte = data[1]
        plaats = data[0]

        ### hier zijn de limits bereikt :
        if plaats=="RD" and int(waterhogte)>=300 and status == "open" :
            reply = "A"   # A is close
            #status = "close"
            message = "De kering gaat dicht. Waterhogte is: "+waterhogte
        elif plaats=="DD" and int(waterhogte)>=290 and status == "open" :
            reply = "A"   # A is close
            status = "close"
            #message = "De kering gaat dicht. Waterhogte is: "+waterhogte
        ### hier zijn de limits niet bereikt :
        elif plaats=="RD" and int(waterhogte)<300 and status == "close" :
            reply = "B" #B is open
            status = "open"
            #message = "De kering gaat open. Waterhogte is: "+waterhogte
        elif plaats=="DD" and int(waterhogte)<290 and status == "close" :
            reply = "B" #B is open
            status = "open"
            #message = "De kering gaat open. Waterhogte is: "+waterhogte
        else:
            continue

        updates = bot.get_updates()
        prints = [u.message.text for u in updates]
        message_ids = [u.message.message_id for u in updates]

        last_command = len(prints) -1
        last_message_id = len(message_ids) -1

        if prints[last_command] == "WISSEL_METING" and message_ids[last_message_id] >= last_message:
            reply = "C"
            message = "Wissel van meetpunt"
            last_message += 1
        connect.sendall(str.encode(reply))
        ### send the update to telegram
        tele_protocol = "https://api.telegram.org/bot520998188:AAEOroYyol_A6A2yIFuzDrgMUZTlX0Y-Ofc/sendMessage?chat_id=409845558&text="
        requests.get(tele_protocol+message)

    connect.close()

def SendMessageBack():
    lijst = [last_message_id_lijst]
    while True:
        last_message_id = bot.get_updates()[-1].message.message_id
        last_message = bot.get_updates()[-1].message.text
        time.sleep(2)
        if last_message == 'WISSEL_MEETPUNT' and lijst == [last_message_id - 1]:
            bot.send_message(chat_id=chat_id, text='Meetpunt gewisseld')
            reply = 'C'
            lijst.clear()
        elif last_message != 'WISSEL_MEETPUNT':
            lijst.clear()
            lijst.append(last_message_id)

SendMessageBack()
while True:
        connect, address = s.accept()
        print('connect from: {0}:{1}'.format(address[0], str(address[1])))

        client_connection(connect)
