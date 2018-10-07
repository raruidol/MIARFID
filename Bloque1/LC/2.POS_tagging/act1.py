import nltk
import random
from nltk.corpus import cess_esp
import pickle


corpus_editable = []

# Corrección del etiquetado base del corpus
def retagging(corpus):

    for frase in range(len(corpus)):
        corpus_editable.append([])
        for palabra_etiquetada in corpus[frase]:

            if palabra_etiquetada[0] == "*0*":
                continue

            if palabra_etiquetada[1][0] == "v" or "F":
                nueva_palabra = (palabra_etiquetada[0], palabra_etiquetada[1][:2])
            else:
                nueva_palabra = (palabra_etiquetada[0], palabra_etiquetada[1][:1])
            corpus_editable[frase].append(nueva_palabra)

    #random.shuffle(corpus_editable)

    # Division del corpus en training 90% y test 10%
    delimiter = round(len(corpus_editable)*0.9)
    training = corpus_editable[:delimiter]
    test = corpus_editable[delimiter:]

    print(len(corpus_editable))
    print(len(training))
    print(len(test))

    return training, test


if __name__ == '__main__':
    corpus = cess_esp.tagged_sents()
    tr, te = retagging(corpus)

    with open('train', 'wb') as fp:
        pickle.dump(tr, fp)

    with open('test', 'wb') as fp:
        pickle.dump(te, fp)
