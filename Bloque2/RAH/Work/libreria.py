import apiai
import json
import sys
import uuid
import requests

key_api = 'AIzaSyCusLiuGP10afHld47NAtg1pR3hAaZCebI'
GOOGLE_BOOKS_API ='https://www.googleapis.com/books/v1/volumes'

def process_turn(utterance=None, debug=False, sid=None):
    booklist = None
    if utterance is None:
        #peticion de inicio del dialogo
        request = ai.event_request(apiai.events.Event("WELCOME"))
        request.lang = 'en'
    elif len(utterance) == 0:
        return None, False, False
    else:
        request = ai.text_request()
        request.query = utterance
#        request.session_id = sid
    response = json.loads(request.getresponse().read().decode('utf8'))
    #process
    if debug:
        print(json.dumps(response, indent=4))
        print(response.keys())
    contexts = response['result']['contexts']
    if len(contexts) > 0 and debug:
        print (list(c['name'] for c in contexts))
    answer = response['result']['fulfillment']['speech']
    double = any([c for c in contexts if c['name'] == 'double'])
    check = any([c for c in contexts if c['name'] == 'check'])
    ask2 = any([c for c in contexts if c['name'] == 'ask2'])
    confirmed = any([c for c in contexts if c['name'] == 'confirmed'])
    canceled = any([c for c in contexts if c['name'] == 'canceled'])

    if double and not check:
        for c in contexts:
            if c['name'] == 'ask':
                print('System: Thank you for your petition, I will check if I can find your book.')
                search = []
                for param in c['parameters']:
                    if c['parameters'][param] != '' and c['parameters'][param] not in search:
                        search.append([param, c['parameters'][param]])
                booklist = get_booklist(search)
                print('System: We found the following books:')
                output(booklist)

    if ask2 and not confirmed:
        for c in contexts:
            if c['name'] == 'check':
                print('System: This is the synopsis you asked for: ')
                syn = get_synopsis(c['parameters']['any'])
                print(syn)

    return answer, confirmed, canceled, booklist

def get_synopsis(code):
    string2 = 'https://www.googleapis.com/books/v1/volumes/'+code
    req2 = requests.get(string2)

    book = req2.json()
    if 'description' in book['volumeInfo']:
        return book['volumeInfo']['description']
    else:
        return 'System: We are sorry, the book has no synopsis.'

def get_booklist(query_list):
    query = []
    for element in query_list:
        if element[0] == 'author':
            query.append('inauthor:'+element[1])

        elif element[0] == 'year':
            query.append('inpublisher:'+element[1])

        elif element[0] == 'genre':
            query.append('subject:'+element[1])

    p = {'key':key_api, 'q':query}
    #req = requests.get(GOOGLE_BOOKS_API, params = p)
    string = 'https://www.googleapis.com/books/v1/volumes?q='
    for el in query:
        string += el+'+'

    req = requests.get(string)

    res = req.json()

    return res

def output(list):
    counter = 0
    print('------------------------------------------------------------')
    if 'items' in list:
        for book in list['items']:
            if counter < 10:
                print('Title: ',book['volumeInfo']['title'])
                print('Id: ',book['id'])
                if 'authors' in book['volumeInfo']:
                    print('Authors: ',book['volumeInfo']['authors'])
                if 'publisher' in book['volumeInfo']:
                    print('Publisher: ',book['volumeInfo']['publisher'])
                if 'publishedDate' in book['volumeInfo']:
                    print('Year: ',book['volumeInfo']['publishedDate'])
                print('------------------------------------------------------------')
                counter += 1
            else:
                break
    else:
        print('Sorry we have found no matches with your requirements.')
        print('------------------------------------------------------------')

if __name__ == "__main__":
    session_id = uuid.uuid4().hex
    CLIENT_ACCESS_TOKEN = "9d6faa16aaeb4aa3acfbf7f627be9907"
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    end = False
    user_turn = None
    while not end:
        if user_turn is not None and len(user_turn) > 0:
            print("User:",user_turn)
        utterance, end, begin, books = process_turn(utterance=user_turn, sid=session_id, debug=False)
        print("System:", utterance)
        if end:

            print('System: We hope our information has been useful.')
            break
        elif begin:
            user_turn = None
        else:
            user_turn = input('-->:')
