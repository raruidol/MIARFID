import pickle
import random
import math
import nltk
import numpy as np
from nltk.tag import hmm
from nltk.tag import tnt
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
for iter in range(10):
    test = bloques[iter]
    train = []
    for element in bloques:
        if element != test:
            for item in element:
                train.append(item)

    # Affix tagger
    suffix_tagger = nltk.tag.AffixTagger(train=train, affix_length=-2)

    # Entrenamiento del etiquetador
    tagger_tnt = tnt.TnT(N=100,unk=suffix_tagger,Trained=True)
    tagger_tnt.train(train)

    # Evaluación del etiquetador
    v = tagger_tnt.evaluate(test)

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

x = [i for i in range(10)]
y = listeval
plt.axis([-1,10,0.9,1])
plt.ylabel("Accuracy")
plt.xlabel("Fold")
plt.title("Ten-fold cross validation TnT shuffled with suffix tagger length = -2")
plt.plot(x, y, "ro")
plt.errorbar(x, y, yerr=desv, linestyle = "None")
plt.show()