import re
import io

with open('entrada_tokenizador.txt', 'r') as f:

    #definir regexs
    regex0 = re.compile(r'(\d{1,2}(:)\d{1,2})'+'|'+'(?:[A-Z]+\.)')

    regex1 = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'+'|'+"\d+\.\d+"+'|'+"\d+\,\d+")

    regex_at = re.compile(r'[^@]+@[^@]+\.[^@]+'+'|'+'@+[^@]+'+'|'+'#+[^#]')

    regex_fm = re.compile(r'(\d{1,2}(/|-)\d{1,2}((/|-)\d{2,4})?)')

    regex_compw = re.compile(r'(\w+(-)\w+)')

    pre_regex = re.compile(r'(\d{2}\w+\d{4})')

    regex_fecha = re.compile(r'(\d{1,2})(\s+)(\w{2})(\s+)(\w+)(\s+)(\w{2})(\s+)(\d{2,4})')


    while True:
        line = f.readline()
        print(line)
        if line == "":
            break

        for item in re.finditer(regex_fecha, line):
            line = regex_fecha.sub('cxz', line)
            aux = item.group()

        for e in line.split():
            if e == 'cxz':
                print(aux)
            elif regex1.match(e):
                print(e)
            elif regex_at.match(e):
                print(e)
            elif regex0.match(e):
                print(e)
            elif regex_fm.match(e):
                print(e)
            elif regex_compw.match(e):
                print(e)

            else:

                regex2 = re.compile('[^#(\w+)]')
                regex3 = re.compile('[#(\w+)]')

                for char in e:
                    if regex2.match(char):
                        print(char)
                        e = e[1:]
                    else:
                        break

                clean1 = regex2.sub('', e)
                if clean1 is not "":
                    print(clean1)
                clean2 = regex3.sub('', e)
                if clean2 is not "":
                    if clean2 == '...':
                        print(clean2)
                    else:
                        for char in clean2:
                            print(char)
