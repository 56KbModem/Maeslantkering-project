import telegram
import time
from sys import exit
bot = telegram.Bot(token= '463188905:AAGm_FknjisEtW68uuNDfAOzBvFI_fdw6GU')
chat_id = bot.get_updates()[-1].message.chat_id

def foutmelding(bot):
    if TAAKHIER <= 0:
        bot.send_message(chat_id= chat_id, text="Er is iets mis met het systeem")

def startimer():
    mins = 0
    if mins == 0:
        while mins != 20:
            time.sleep(60)
            mins += 1
    else:
        exit(0)


def updater(bot):
    updates = bot.get_updates()
    print([u.message.text for u in updates])
    while startimer() != 20:
        if ([u.message.text for u in updates]) == '1':
            bot.send_message(chat_id= chat_id, text='Poort gaat open')
        elif ([u.message.text for u in updates]) == '2':
            bot.send_message(chat_id= chat_id, text='Poort gaat dicht')
        elif ([u.message.text for u in updates]) == '3':
            bot.send_message(chat_id= chat_id, text='Poort gaat half open')
        else:
            break



updater(bot)
