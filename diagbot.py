import json
from os.path import getmtime
from threading import Thread
from time import sleep

from pyswip import Prolog
from telegram.bot import Bot
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
from telegram.utils.request import Request

from handlers import start, summarize
from textProcessing import WordProcessing


class DiagBot(WordProcessing, Bot, Thread):
    def __init__(self, token):
        request = Request(con_pool_size=8, proxy_url='http://144.217.160.173:3128')
        Bot.__init__(self, request=request, token=token)
        Thread.__init__(self)

        self.prolog = Prolog()
        self.prolog.consult('rules.pl')

        self._filename = "file.json"
        self._file_mdate = getmtime(self._filename)

        self.updater = Updater(bot=self)
        self.dispatcher = self.updater.dispatcher

        self.chat_id = 0

        self.dispatcher.add_handler(CommandHandler('start', start))
        self.dispatcher.add_handler(MessageHandler(Filters.text, summarize))

        self.updater.start_polling()
        self.start()

    def extract_symptoms(self, text):
        symptoms = self.process(text)
        with open(self._filename, "w") as file:
            json.dump(symptoms, file)

    def _consult(self):
        with open(self._filename, "r") as file:
            symptoms = json.load(file)
        print(symptoms)
        answer = list(self.prolog.query(f'identify(X, {symptoms})'))
        if answer:
            diag = answer[0]['X']
            diag = diag.replace('_', ' ')
            diag = 'Вероятно, у вас ' + diag.encode('utf-8').decode('utf-16')
        else:
            diag = "Не удалось определить диагноз"

        return diag

    def run(self):
        while True:
            print(self._file_mdate, getmtime(self._filename))
            if self._file_mdate != getmtime(self._filename):
                diag = self._consult()

                self.sendMessage(chat_id=self.chat_id,
                                 text=diag)
            sleep(0.5)

