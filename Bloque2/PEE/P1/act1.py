import pandas as pd
import math

for i in range(1,5):

    vals = pd.read_csv("probg"+str(i)+".txt", header = None)
    valsViterbi = pd.read_csv("probVg"+str(i)+".txt", header = None)

    listval = vals[0].tolist()
    listvalviterbi = valsViterbi[0].tolist()

    logprob = 0
    prob = 0
    log2prob = 0
    for val in listval:
        log2prob += math.log2(val)
        logprob += math.log(val)
        prob += val

    perplex = math.pow(2, (-(1/1000))*log2prob)

    probvit = 0
    logprobvit = 0
    for vitval in listvalviterbi:
        probvit += vitval
        logprobvit += math.log(vitval)


    print("The probabilistic grammar"+str(i)+" :")
    print("Likelihood: ", prob)
    print("Log-ikelihood: ", logprob)
    print("Viterbi likelihood: ", probvit)
    print("Viterbi log-likelihood: ", logprobvit)
    print("Test Set Perplexity: ", perplex)
    print("----------------------------------------")
