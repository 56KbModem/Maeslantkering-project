import telegram
import time

bot = telegram.Bot(token= '463188905:AAGm_FknjisEtW68uuNDfAOzBvFI_fdw6GU')
chat_id = bot.get_updates()[-1].message.chat_id
last_message_id_lijst = bot.get_updates()[-1].message.message_id

def SendMessageBack():
    lijst = [last_message_id_lijst]
    while True:
        last_message_id = bot.get_updates()[-1].message.message_id
        print(last_message_id)
        last_message = bot.get_updates()[-1].message.text
        print(last_message)
        print(lijst)
        time.sleep(2)
        if last_message == 'WISSEL_MEETPUNT' and lijst == [last_message_id - 1]:
            bot.send_message(chat_id=chat_id, text='Meetpunt gewisseld')
            reply = 'C'
            lijst.clear()
            print(lijst)
        elif last_message != 'WISSEL_MEETPUNT':
            lijst.clear()
            lijst.append(last_message_id)
            print('Andere Message')

SendMessageBack()
