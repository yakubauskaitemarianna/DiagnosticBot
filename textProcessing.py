from nltk.corpus import wordnet
from pyswip import Prolog

class BaseDate:
    symptoms_base1 = ['nasal congestion', 'itchy eyes', 'sneezing', 'sore throat',
                 'cough', 'abdominal pain', 'back pain', 'chills', 'constipation',
                 'diarrhea', 'fever', 'loss of appetite', 'malaise', 'nausea',
                 'painful rination', 'rectal pain', 'vomiting', 'joint pain',
                 'rash', 'nausea', 'muscle pain', 'fatigue', 'hunger',
                 'urination changes', 'thirst changes', 'weight changes',
                 'fatigue', 'vomiting', 'blurredvision', 'dry mouth', 'itch',
                 'slow-healing wounds', 'absent menstrual periods',
                 'breast pain', 'food aversion', 'frequent urination', 'headache',
                 'mood changes', 'tiredness', 'vomiting', 'urination changes',
                 'pain urination', 'erectile dysfunction', 'painful ejaculation',
                 'blood in urine', 'weight loss', 'bone pain', 'swelling', 'malaise',
                 'headache', 'muscle pain', 'tiredness', 'fatigue', 'appetite loss',
                 'diarrhea', 'itch', 'burning', 'tingling', 'swollen lymph nodes',
                 'joint pain', 'night sweats', 'mouth ulcers', 'vaginal dryness',
                 'painful sexual intercourse', 'vaginal irritation', 'acne']

    symptoms_base = ['thirst_changes', 'tiredness', 'sneezing', 'blood_in_urine',
    'itchy_eyes', 'vaginal_irritation', 'urination_changes', 'abdominal_pain',
    'slow-healing_wounds', 'painful_ejaculation', 'loss_of_appetite', 'rash',
    'frequent_urination', 'swelling', 'fatigue', 'appetite_loss', 'mouth_ulcers',
    'pain_urination', 'cough', 'headache', 'acne', 'swollen_lymph_nodes',
    'night_sweats', 'bone_pain', 'burning', 'constipation', 'sore_throat',
    'erectile_dysfunction', 'dry_mouth', 'vaginal_dryness', 'rectal_pain',
    'breast_pain', 'nausea', 'muscle_pain', 'back_pain', 'fever', 'joint_pain',
    'vomiting', 'chills', 'blurred_vision', 'tingling', 'food_aversion',
    'weight_loss', 'nasal_congestion', 'malaise', 'diarrhea', 'itch',
    'painful_sexual_intercourse', 'absent_menstrual_periods', 'hunger',
    'weight_changes', 'mood_changes', 'loss_of_appetite']



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
    text = 'i have a terrible rhinal mother pain loss of appetite tiredness'
    text = text.split()
    results = []
    for i in range(len(text)):
        result = WordProcessing.extract_symptoms_base(text[i], BaseDate.symptoms_base)
        if result != '':
            results.append(result)

    prolog_data = []
    flag = 0
    for i in range(len(results) - 1):
        for j in range(len(BaseDate.symptoms_base)):
            if results[i] == BaseDate.symptoms_base[j]:
                prolog_data.append(results[i])
            if str(results[i] + '_' + results[i+1]) in BaseDate.symptoms_base[j]:
                prolog_data.append(BaseDate.symptoms_base[j])
            if results[-1] == BaseDate.symptoms_base[j] and flag == 0:
                prolog_data.append(BaseDate.symptoms_base[j])
                flag = 1

text_symps = 'itchy eyes sore throat sneezing'
text_symps = text_symps.split()
results = []
for i in range(len(text_symps)):
    result = WordProcessing.extract_symptoms_base(text_symps[i],
                                                  BaseDate.symptoms_base)
    if result != '':
        results.append(result)

prolog_data = []
flag = 0
for i in range(len(results) - 1):
    for j in range(len(BaseDate.symptoms_base)):
        if results[i] == BaseDate.symptoms_base[j]:
            prolog_data.append(results[i])
        if str(results[i] + '_' + results[i+1]) in BaseDate.symptoms_base[j]:
            prolog_data.append(BaseDate.symptoms_base[j])
        if results[-1] == BaseDate.symptoms_base[j] and flag == 0:
            prolog_data.append(BaseDate.symptoms_base[j])
            flag = 1

prolog = Prolog()
prolog.consult('rules.pl')

answer = list(prolog.query(f'identify(X, {prolog_data})'))
diag = answer[0]['X']
print(diag)