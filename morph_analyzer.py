from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import textProcessing

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token='843122829:AAGy3knNMBy4BItZBrhAgYUqnMMjJpS0SxY',
                  request_kwargs={
                          'proxy_url': 'https://167.114.255.85:3128'
                          })
dispatcher = updater.dispatcher

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Hi. Send me any English text and I'll summarize it for you.")

def summarize(bot, update):
    try:
        text = update.message.text
        #print(">>>> ",text, type(text), ">>>")
        text = text.split()
        # before Prolog part
        results = []
        for i in range(len(text)):
            result = textProcessing.WordProcessing.extract_symptoms_base(text[i],
                                                          BaseDate.symptoms_base)
            if result != '':
                results.append(result)

        # Паша, тебе в Prolog идет массив results, который из исходного текста
        # содержит те слова, которые есть в нашей базе textProcessing.BaseDate.symptoms_base

        # after Prolog part
        # пока я пользователю возвращаю Hello world
        bot.sendMessage(chat_id=update.message.chat_id,
                        text='Hello world')
    except UnicodeEncodeError:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Sorry, but I can't summarise your text.")

start_handler = CommandHandler('start', start)

summarize_handler = MessageHandler([Filters.text], summarize)

dispatcher.add_handler(summarize_handler)
dispatcher.add_handler(start_handler)

updater.start_polling()
