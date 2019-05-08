from nltk.corpus import wordnet

class BaseDate:
    symptoms_base = ['nasal congestion', 'itchy eyes', 'sneezing', 'sore throat',
                 'cough', 'abdominal pain', 'back pain', 'chills', 'constipation',
                 'diarrhea', 'fever', 'loss of appetite', 'malaise', 'nausea',
                 'rectal pain', 'vomiting', 'joint pain',
                 'rash', 'nausea', 'muscle pain', 'fatigue', 'hunger',
                 'urination changes', 'thirst changes', 'weight changes',
                 'fatigue', 'vomiting', 'blurred vision', 'dry mouth', 'itch',
                 'slow-healing wounds', 'absent menstrual periods',
                 'breast pain', 'food aversion', 'frequent urination', 'headache',
                 'mood changes', 'tiredness', 'vomiting', 'urination changes',
                 'pain urination', 'erectile dysfunction', 'painful ejaculation',
                 'blood in urine', 'weight loss', 'bone pain', 'swelling', 'malaise',
                 'headache', 'muscle pain', 'tiredness', 'fatigue', 'appetite loss',
                 'diarrhea', 'itch', 'burning', 'tingling', 'swollen lymph nodes',
                 'joint pain', 'night sweats', 'mouth ulcers', 'vaginal dryness',
                 'painful sexual intercourse', 'vaginal irritation', 'acne']

class WordProcessing(BaseDate):
    def __init__(self, user_string, text):
        self.user_string = user_string
        self.text = text

    def extract_symptoms_base(user_string, symptoms_base):

        def check_word(word, base):
            for i in range(len(base)):
                for j in range(len(base[i])):
                    if base[i][j] == word:
                        return base[i][j]
                    else:
                        continue

        symptoms_base = [symptoms_base[i].split() for i in range(len(symptoms_base))]
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

text = 'i have a terrible nasal desease'
text = text.split()
results = []
for i in range(len(text)):
    result = WordProcessing.extract_symptoms_base(text[i], BaseDate.symptoms_base)
    if result != '':
        results.append(result)

print(results)
