from nltk.corpus import wordnet
from pyswip import Prolog
import json
import itertools
import pymorphy2
import string

class BaseDate:
    symptoms_base_dict = {'жажда' : 'thirst_changes', 'усталость' : 'tiredness',
    'чихать' : 'sneezing', 'кровь_в_моче' : 'blood_in_urine', 'недомогание' : 'malaise',
    'сухость_в_глазах' : 'itchy_eyes', 'размытое_зрение' : 'blurred_vision',
    'изменения_мочеиспускания' : 'urination_changes', 'боль_в_животе' : 'abdominal_pain',
     'медленно_заживающие_раны' : 'slow-healing_wounds', 'сыпь' : 'rash',
     'боль_при_эакуляции' : 'painful_ejaculation', 'припухлость' : 'swelling',
     'потеря_аппетита' : 'loss_of_appetite', 'акне' : 'acne', 'лихорадка' : 'fever',
    'частое_мочеиспускание' : 'frequent_urination', 'головная_боль' : 'headache',
    'усталость' : 'fatigue', 'язвы_во_рту' : 'mouth_ulcers', 'кашель' : 'cough',
    'мочеиспускание_с_болью' : 'pain_urination', 'жжение' : 'burning',
    'увеличение_лимфатических_узлов' : 'swollen_lymph_nodes', 'зуд' : 'itch',
    'ночной_пот' : 'night_sweats', 'боль_в_костях' : 'bone_pain',
    'больное_горло' : 'sore_throat', 'запор' : 'constipation',
    'сухость_во_рту' : 'dry_mouth', 'вагинальная_сухость' : 'vaginal_dryness',
    'ректальная_боль' : 'rectal_pain', 'боль_в_груди' : 'breast_pain',
    'тошнота' : 'nausea', 'мышечная_боль' : 'muscle_pain',
    'раздражение_влагалища' : 'vaginal_irritation', 'боль_в_спине' : 'back_pain',
    'боль_в_суставах' : 'joint_pain', 'рвота' : 'vomiting', 'озноб' : 'chills',
    'покалывание' : 'tingling', 'неприятие_пищи' :  'food_aversion',
    'потеря_веса' : 'weight_loss', 'заложенность_носа' : 'nasal_congestion',
    'голод' : 'hunger', 'болезненный_половой_акт' : 'painful_sexual_intercourse',
    'диарея' : 'diarrhea', 'отстутствие_менструации' : 'absent_menstrual_periods',
    'изменение_веса' : 'weight_changes', 'изменение_настроения' : 'mood_changes',
    'эриктильная_дисфункция' : 'erectile_dysfunction'}

class WordProcessing(BaseDate):
    def __init__(self, user_string, text):
        self.user_string = user_string
        self.text = text

    @staticmethod
    def extract_symptoms_base(user_string, symptoms_base):

        def check_word(word, base):
            for i in range(len(base)):
                for j in range(len(base[i])):
                    if base[i][j] == word:
                        return base[i][j]
                    else:
                        continue

        symptoms_base = [symptoms_base[i].split('_') for i in range(len(symptoms_base))]
        if check_word(user_string, symptoms_base) == user_string:
            return user_string

        user_string_syns = wordnet.synsets(user_string)
        result = ''
        for i in range(len(user_string_syns)):
            syns = [str(lemma.name()) for lemma in user_string_syns[i].lemmas()]
            for j in range(len(syns)):
                if check_word(syns[j], symptoms_base) == syns[j]:
                    result = syns[j]
        return result

    @staticmethod
    def symptoms_combination(maxlen, extracted_sympt):
        results = []
        for count in range(0, maxlen + 1):
            for extracted in itertools.combinations(extracted_sympt, count):
                    results.append('_'.join(extracted))
        return results

if __name__ == "__main__":
    text1 = 'i have a terrible rhinal swelling sore throat and itchy eyes'
    text1 = 'acne'
    text = 'Я чихаю, у меня сухость в глазах и больное горло.'

    text = "".join(l for l in text if l not in string.punctuation)
    text = (text.lower()).split()

    results = []
    symptoms_base_ru = [symptoms for symptoms, values in BaseDate.symptoms_base_dict.items()]

    morph = pymorphy2.MorphAnalyzer()

    for i in range(len(text)):
        result = WordProcessing.extract_symptoms_base(text[i], symptoms_base_ru)
        if result != '':
            results.append(result)
        else:
            normal_form = morph.parse(text[i])[0].normal_form
            result = WordProcessing.extract_symptoms_base(normal_form, symptoms_base_ru)
            if result:
                results.append(result)

    prolog_data = []
    flag = 0

    _maxcount = max([word.count('_') for word in symptoms_base_ru]) + 1

    results = WordProcessing.symptoms_combination(_maxcount, results)

    for i in range(len(results)):
        for j in range(len(symptoms_base_ru)):
            if results[i] == symptoms_base_ru[j]:
                prolog_data.append(results[i])


    prolog_data = list(dict.fromkeys(prolog_data))
    print(prolog_data)

    results = [BaseDate.symptoms_base_dict.get(prolog_data[i]) for i in range(len(prolog_data))]

    print(results)
'''
    prolog = Prolog()
    prolog.consult('rules.pl')
    answer = list(prolog.query(f'identify(X, {results})'))
    #print(answer)
    if answer:
        diag = answer[0]['X']
        diag = diag.replace('_', ' ')
        print('Maybe you have a', diag.encode('utf-8').decode('utf-16'))
    else:
        print("Can't identify")
'''
