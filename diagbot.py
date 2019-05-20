from textProcessing import WordProcessing
from telegram.bot import Bot
from pyswip import Prolog
import json


class DiagBot(WordProcessing, Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prolog = Prolog()
        self.prolog.consult('rules.pl')

    def extract_symptoms(self, text):
        symptoms = self.process(text)
        with open("file.json", "w") as file:
            json.dump(symptoms, file)

    def consult(self):
        with open("file.json", "r") as file:
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
