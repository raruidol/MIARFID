import pickle
import random
import math
import nltk
from nltk.tag import hmm
from nltk.tag import UnigramTagger
from nltk.corpus import treebank
from nltk.tag import brill
from nltk.tbl.template import Template
from nltk.tag.brill import Pos, Word
from nltk.tag import brill_trainer
from nltk.tag import crf
from nltk.tag import perceptron
import matplotlib.pyplot as plt

with open('test', 'rb') as fp:
    test = pickle.load(fp)

with open('train', 'rb') as fp:
    train = pickle.load(fp)

corpus = test+train
random.shuffle(corpus)

jump = round(len(corpus)/10)

bloques = []
delimiter = 0

# Construyo los 10 bloques para la validación cruzada
for i in range(10):

    bloques.append(corpus[delimiter:delimiter+jump])
    delimiter = delimiter+jump

listeval = []
intervals = []
for iter in range(10):
    test = bloques[iter]
    train = []
    for element in bloques:
        if element != test:
            for item in element:
                train.append(item)

    # Entrenamiento del etiquetador

    '''
    
    # Brill tagger
    baseline_data = train
    #baseline = UnigramTagger(baseline_data)
    baseline = hmm.HiddenMarkovModelTagger.train(baseline_data)
    templates = [Template(Pos([-1])), Template(Pos([-1]), Word([0]))]
    tagger_brill_tr = brill_trainer.BrillTaggerTrainer(initial_tagger=baseline, templates=templates, trace=3)
    tagger_brill = tagger_brill_tr.train(train, max_rules=10)
    '''

    # CRF taffer
    tagger_crf = crf.CRFTagger()
    tagger_crf.train(train, "model")
    print("CRF Fold", iter)

    # Perceptron tagger
    #tagger_perceptron = perceptron.PerceptronTagger()
    #tagger_perceptron.train(train)


    # Evaluación del etiquetador
    v = tagger_crf.evaluate(test)

    d = 1.96*math.sqrt((v*(1-v))/len(test))
    ic = [round(v-d,3),round(v+d, 3)]

    listeval.append(round(v, 3))
    intervals.append(ic)


v=0
for val in listeval:
    v += val
va = v/10
print(listeval)
print(intervals)

desv = 1.96*math.sqrt((va*(1-va))/len(test))
ic = [round(va-desv, 3),round(va+desv, 3)]
print(round(va, 3))
print(ic)

x = [i for i in range(10)]
y = listeval
plt.axis([-1,10,0.8,1])
plt.ylabel("Accuracy")
plt.xlabel("Fold")
plt.title("Ten-fold cross validation CRF tagger")
plt.plot(x, y, "ro")
plt.errorbar(x, y, yerr=desv, linestyle = "None")
plt.show()