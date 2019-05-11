from nltk.corpus import wordnet
from pyswip import Prolog
import json

class BaseDate:
    symptoms_base_dict = {'жажда' : 'thirst_changes', 'усталость' : 'tiredness',
    'чихание' : 'sneezing', 'кровь_в_моче' : 'blood_in_urine',
    'сухость_в_глазах' : 'itchy_eyes', 'раздражение_влагалища' : 'vaginal_irritation',
    'изменения_мочеиспускания' : 'urination_changes', 'боль_в_животе' : 'abdominal_pain',
     'медленно_заживающие_раны' : 'slow-healing_wounds', 'боль_при_эакуляции' : 'painful_ejaculation',
    'потеря_аппетита' : 'loss_of_appetite', 'сыпь' : 'rash',
    'частое_мочеиспускание' : 'frequent_urination', 'припухлость' : 'swelling',
    'усталость' : 'fatigue', 'потеря_аппетита' : 'appetite_loss',
    'язвы_во_рту' : 'mouth_ulcers', 'мочеиспускание_с_болью' : 'pain_urination',
    'кашель' : 'cough', 'головная_боль' : 'headache', 'акне' : 'acne',
    'увеличение_лимфатических_узлов' : 'swollen_lymph_nodes', 'ночной_пот' : 'night_sweats',
    'боль_в_костях' : 'bone_pain', 'жжение' : 'burning', 'запор' : 'constipation',
    'больное_горло' : 'sore_throat', 'эриктильная_дисфункция' : 'erectile_dysfunction',
    'сухость_во_рту' : 'dry_mouth', 'вагинальная_сухость' : 'vaginal_dryness',
    'ректальная_боль' : 'rectal_pain', 'боль_в_груди' : 'breast_pain',
    'тошнота' : 'nausea', 'мышечная_боль' : 'muscle_pain',
    'боль_в_спине' : 'back_pain', 'лихорадка' : 'fever', 'боль_в_суставах' : 'joint_pain',
    'рвота' : 'vomiting', 'озноб' : 'chills', 'размытое_зрение' : 'blurred_vision',
    'покалывание' : 'tingling', 'неприятие_пищи' :  'food_aversion',
    'потеря_веса' : 'weight_loss', 'заложенность_носа' : 'nasal_congestion',
    'недомогание' : 'malaise', 'диарея' : 'diarrhea', 'зуд' : 'itch',
    'болезненный_половой_акт' : 'painful_sexual_intercourse',
    'отстутствие_менструации' : 'absent_menstrual_periods', 'голод' : 'hunger',
    'изменение_веса' : 'weight_changes', 'изменение_настроения' : 'mood_changes'}

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

if __name__ == "__main__":
    text1 = 'i have a terrible rhinal swelling sore throat and itchy eyes'
    text1 = 'acne'
    text = 'я чихаю у меня сухость в глазах и больное горло'
    text = text.split()

    results = []
    symptoms_base_ru = [symptoms for symptoms, values in BaseDate.symptoms_base_dict.items()]

    for i in range(len(text)):
        result = WordProcessing.extract_symptoms_base(text[i], symptoms_base_ru)
        if result != '':
            results.append(result)

    prolog_data = []
    flag = 0
    for i in range(len(results) - 1):
        for j in range(len(symptoms_base_ru)):
            if results[i] == symptoms_base_ru[j]:
                prolog_data.append(results[i])
            if str(results[i] + '_' + results[i+1]) in symptoms_base_ru[j]:
                prolog_data.append(symptoms_base_ru[j])
            if results[-1] == symptoms_base_ru[j] and flag == 0:
                prolog_data.append(symptoms_base_ru[j])
                flag = 1

    prolog_data = list(dict.fromkeys(prolog_data))
    print(prolog_data)
'''
	#.encode('utf-8').decode('cp866')
    prolog_data = list(map((lambda x : x.encode('utf-16').decode('utf-8')),["чихание", "сухость_в_глазах", "больное_горло"]))
    #print(prolog_data)

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
