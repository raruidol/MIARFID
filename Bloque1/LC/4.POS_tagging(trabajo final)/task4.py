import pickle
import random
import math
import numpy as np
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

random.seed(1)

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
random.shuffle(bloques)
for iter in range(10):
    test = bloques[iter]
    train = []
    for element in bloques:
        if element != test:
            for item in element:
                train.append(item)

    # Entrenamiento del etiquetador


    # Brill tagger
    baseline_data = train
    baseline = UnigramTagger(baseline_data)
    #baseline = hmm.HiddenMarkovModelTagger.train(baseline_data)
    templates = [Template(Pos([-1])), Template(Pos([-1]), Word([0]))]
    tagger_brill_tr = brill_trainer.BrillTaggerTrainer(initial_tagger=baseline, templates=templates, trace=3)
    tagger_brill = tagger_brill_tr.train(train, max_rules=10)


    '''
    # CRF tagger
    tagger_crf = crf.CRFTagger()
    tagger_crf.train(train, "model")
    print("CRF Fold", iter)
    '''

    '''
    # Perceptron tagger
    tagger_perceptron = perceptron.PerceptronTagger(load = False)
    tagger_perceptron.train(train)
    '''

    # Evaluación del etiquetador
    v = tagger_brill.evaluate(test)

    d = 1.96*math.sqrt((v*(1-v))/len(np.array(test).flatten())/2)
    ic = [round(v-d,3),round(v+d, 3)]

    listeval.append(round(v, 3))
    intervals.append(ic)


v=0
for val in listeval:
    v += val
va = v/10
print(listeval)
print(intervals)

desv = 1.96*math.sqrt((va*(1-va))/len(np.array(test).flatten())/2)
ic = [round(va-desv, 3),round(va+desv, 3)]
print(round(va, 3))
print(ic)
'''

va = sum(listeval) / 10
desv = math.sqrt(1.96*np.var(listeval)/10)
ic = [round(va-desv, 5),round(va+desv, 5)]
print(round(va, 5))
print(ic)
'''
x = [i for i in range(10)]
y = listeval
plt.axis([-1,10,0.7,1])
plt.ylabel("Accuracy")
plt.xlabel("Fold")
plt.title("Ten-fold cross validation Brill tagger")
plt.plot(x, y, "ro")
plt.errorbar(x, y, yerr=desv, linestyle = "None")
plt.show()