import time
from datetime import datetime
import MetaTrader5 as mt5
import ozo.judaswing as tJswing
import os
import telebot
import ozo.news as oNews

if not mt5.initialize():
    print("Initialize failed")
    mt5.shutdown()

n = oNews.News()
jswing = tJswing.Judaswing()
# msnr = oMsnr.Msnr()
bot = telebot.TeleBot('6911546574:AAEg8NM0NMcagHlzEbJEWeYyRz7h0cQKuHI')


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    while True:
        bot.reply_to(message, "checking news")
        if n.check_forex_day('https://www.forexfactory.com/calendar?day=today') == "Good day":
            bot.reply_to(message, "Good day, Starting with judas swing: ")
            if jswing.start(bot, message):
                bot.reply_to(message, "The bot has finished trading today now sleeping until tmrow")
        else:
            bot.reply_to(message, "Bad day, checking tomorrow if it's a good day:")
        if n.check_forex_day('https://www.forexfactory.com/calendar?day=tomorrow') == "Good day":
            next_midnight = datetime.now().replace(hour=23, minute=59, second=0)
            delta = next_midnight - datetime.now()
            print(delta)
            time.sleep(delta.total_seconds() + 90)
        else:
            next_midnight = datetime.now().replace(hour=23, minute=59, second=0)
            delta = next_midnight - datetime.now()
            print(delta)
            time.sleep(86400 + delta.total_seconds() + 90)


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
