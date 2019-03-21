# PARSER xml pràctica 2 minidom#

# Parser del TRAIN #
from xml.dom import minidom

xmldoc = minidom.parse('TASS2017_T1_test.xml')
tweets = xmldoc.getElementsByTagName('tweet')
# outfile = open('training.txt', 'w')
for t in tweets:
    for node in t.childNodes:
        # print (t.childNodes)
        if node.nodeName == 'tweetid':
            id_t = node.firstChild.data
        elif node.nodeName == 'content':
            text_t = node.firstChild.data.replace("\n", " ")

        elif node.nodeName == 'sentiment':
            for h in node.childNodes:
                if h.nodeName == 'polarity':
                    if h.firstChild.nodeName == 'value':
                        pol_t = h.firstChild.firstChild.data
    print(id_t, pol_t, text_t)
