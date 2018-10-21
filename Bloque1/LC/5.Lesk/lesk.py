import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords as sw

def compute_overlap(context, signature):
    ov = 0
    for word in context:
        if word in signature:
            ov += 1

    return ov


def simpLesk(word, sentence):
    best_sense = None
    max_overlap = 0
    t_sent = nltk.word_tokenize(sentence)
    context = []
    for w in t_sent:
        if w not in sw.words('english'):
            context.append(w)
    senses = wn.synsets(word)
    for s in senses:
        signature = []
        defin = s.definition()
        for z in nltk.word_tokenize(defin):
            signature.append(z)
        examp = s.examples()
        for z in examp:
            signature.append(z)

        overlap = compute_overlap(context, signature)

        if overlap > max_overlap:
            max_overlap = overlap
            best_sense = s

    return best_sense


if __name__ == '__main__':
    w = "bank"
    s = "Yesterday I went to the bank to withdraw the money and the credit card did not work"
    print(simpLesk(w, s))
