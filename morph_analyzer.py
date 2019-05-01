from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import textProcessing

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token='HAHAHAHAHA',
                  request_kwargs={
                          'proxy_url': 'https://167.114.255.85:3128'
                          })
dispatcher = updater.dispatcher

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Hi. Send me any symptoms and I'll summarize it for you.")

def summarize(bot, update):
    try:
        text = update.message.text
        text = textProcessing.morphing(text)
        print(">>>> ",text, ">>>")
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Hello world')
    except UnicodeEncodeError:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Sorry, but I can't define your symphoms. Maybe you are dying...")

start_handler = CommandHandler('start', start)

summarize_handler = MessageHandler([Filters.text], summarize)

dispatcher.add_handler(summarize_handler)
dispatcher.add_handler(start_handler)

updater.start_polling()
