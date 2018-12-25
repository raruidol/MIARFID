import pandas as pd
import math

for i in range(1,5):

    vals = pd.read_csv("probor"+str(i)+".txt", header = None)

    listval = vals[0].tolist()

    palindromes = 0
    apm = 0
    for val in listval:
        if val != 0:
            palindromes += 1
            apm += val


    print("The probabilistic grammar"+str(i)+" :")
    print("Palindromes: ", palindromes)
    print("apm: ", apm)