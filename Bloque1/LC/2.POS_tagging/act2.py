from nltk.tag import hmm
from nltk.tag import tnt
import pickle
import numpy

with open('test', 'rb') as fp:
    test = pickle.load(fp)

with open('train', 'rb') as fp:
    train = pickle.load(fp)

# Entrenamiento del etiquetador
#tagger_hmm = hmm.HiddenMarkovModelTagger.train(train)
tagger_tnt = tnt.TnT()
tagger_tnt.train(train)

# Evaluación del etiquetador
#print(tagger_hmm.evaluate(test))
print(tagger_tnt.evaluate(test))

# Etiquetado de palabras del conjunto de test
words=[]
correct = []
for sentence in test:
    for word in sentence:
        words.append(word[0])
        correct.append(word)

#t = tagger_hmm.tag(words)
t = tagger_tnt.tag(words)

for w,c in t:
    print(w,"/",c)

print("----------------------")

print(correct)