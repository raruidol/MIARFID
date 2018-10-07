def act1(cadena):
    tokens = cadena.split(" ")
    listoftypes=[]
    for token in tokens:
        listoftypes.append(token.split("/"))
    dict = {}
    for element in listoftypes:
        if element[1] in dict:
            dict[element[1]] += 1
        else:
            dict[element[1]] = 1
    res = []
    for key in sorted(dict.keys()):
        res.append([key, dict[key]])
    return res


def act2(cadena):
    tokens = cadena.lower().split(" ")
    listoftypes=[]
    for token in tokens:
        listoftypes.append(token.split("/"))
    dict1 = {}
    for element in listoftypes:
        if element[0] in dict1:
            dict1[element[0]][0] += 1
            if element[1] in dict1[element[0]][1]:
                dict1[element[0]][1][element[1]] += 1
            else:
                dict1[element[0]][1].update({element[1]:1})
        else:
            dict1[element[0]] = [1, {element[1]:1}]
    res = []
    for key in sorted(dict1.keys()):
        res.append([key, dict1[key]])
    return res

def act3(cadena):
    tokens = cadena.lower().split(" ")
    listoftypes=[]
    for token in tokens:
        listoftypes.append(token.split("/"))
    duplas = []
    for i in range(0, len(listoftypes)-1):
        dupla = ([listoftypes[i][1], listoftypes[i+1][1]])
        duplas.append(dupla)
    duplas.insert(0, ["<S>", dupla[1][0]])
    duplas.append([dupla[len(dupla)-1][0], "</S>"])
    counted = []
    res = []
    for dupla in duplas:
        count = 0
        if dupla not in counted:
            for j in range(0, len(duplas)):
                if dupla == duplas[j]:
                    count+=1
        counted.append(dupla)
        if count>0:
            res.append([dupla, count])
    return res

def act4(numtypes, numwords, word):
    for element in numwords:
        if word in element:
            for key in element[1][1].keys():
                for n in numtypes:
                    if key.upper() in n:
                        val1 = n[1]
                val2 = element[1][0]
                val3 = element[1][1][key]
                print("P("+word+" | "+key.upper()+") = ", val3/val1)
                print("P("+key.upper()+" | "+word+") = ", val3/val2)


if __name__ == '__main__':
    cadena ="El/DT perro/N come/V carne/N de/P la/DT carnicería/N y/C de/P la/DT nevera/N y/C canta/V el/DT la/N la/N la/N ./Fp"
    print("Actividad 1 resultado:")
    sol1 = act1(cadena)
    for element in sol1:
        print(element[0], element[1])
    print("Actividad 2 resultado:")
    sol2 = act2(cadena)
    for element in sol2:
        print(element[0], element[1])
    print("Actividad 3 resultado:")
    sol3 = act3(cadena)
    for element in sol3:
        print(element[0], element[1])
    print("Actividad 4 resultado:")
    print("Introduzca la palabra deseada")
    w = input()
    sol4=act4(sol1, sol2, w)
