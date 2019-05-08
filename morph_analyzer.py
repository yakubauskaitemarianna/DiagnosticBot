from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import textProcessing
from pyswip import Prolog

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(token='',
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
                                                          textProcessing.BaseDate.symptoms_base)
            if result != '':
                results.append(result)

        prolog_data = []
        flag = 0
        for i in range(len(results) - 1):
            for j in range(len(textProcessing.BaseDate.symptoms_base)):
                if results[i] == textProcessing.BaseDate.symptoms_base[j]:
                    prolog_data.append(results[i])
                if str(results[i] + '_' + results[i+1]) in textProcessing.BaseDate.symptoms_base[j]:
                    prolog_data.append(textProcessing.BaseDate.symptoms_base[j])
                if results[-1] == textProcessing.BaseDate.symptoms_base[j] and flag == 0:
                    prolog_data.append(textProcessing.BaseDate.symptoms_base[j])
                    flag = 1
                    
        prolog = Prolog()
        prolog.consult('rules.pl')
        answer = list(prolog.query(f'identify(X, {results})'))
        diag = answer[0]['X']
        
        bot.sendMessage(chat_id=update.message.chat_id,
                         text=diag)
    except UnicodeEncodeError:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Sorry, but I can't summarise your text.")

start_handler = CommandHandler('start', start)

summarize_handler = MessageHandler([Filters.text], summarize)

dispatcher.add_handler(summarize_handler)
dispatcher.add_handler(start_handler)

updater.start_polling()
