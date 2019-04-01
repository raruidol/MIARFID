from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from nltk.tokenize.casual import casual_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import accuracy_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import SGDClassifier
from sklearn import neighbors
import re
from nltk.corpus import stopwords

def load():
    train_text = []
    train_target = []
    dev_text = []
    dev_target = []
    test_id = []
    test_text = []

    with open('P2/train_text.txt') as f:
        for text in f:
            train_text.append(text)

    with open('P2/train_pol.txt') as f:
        for text in f:
            train_target.append(text)

    with open('P2/dev_text.txt') as f:
        for text in f:
            dev_text.append(text)

    with open('P2/dev_pol.txt') as f:
        for text in f:
            dev_target.append(text)

    with open('P2/test_id.txt') as f:
        for text in f:
            test_id.append(text)

    with open('P2/test.txt') as f:
        for text in f:
            test_text.append(text)

    return train_text, train_target, dev_text, dev_target, test_text, test_id

# Preprocessing

def preprocess(train_text, dev_text, test_text):

    clean_train = []
    clean_dev = []
    clean_test = []

    regex_at = re.compile(r'@+\w+' + '|' + '#+\w+')
    regex_url = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')

    print('Cleaning...')
    for element in train_text:
        for item in re.finditer(regex_at, element):
            element = regex_at.sub('>twit', element)
        for item in re.finditer(regex_url, element):
            element = regex_url.sub('>url', element)
        clean_train.append(element)

    for element in dev_text:
        for item in re.finditer(regex_at, element):
            element = regex_at.sub('>twit', element)
        for item in re.finditer(regex_url, element):
            element = regex_url.sub('>url', element)
        clean_dev.append(element)

    for element in test_text:
        for item in re.finditer(regex_at, element):
            element = regex_at.sub('>twit', element)
        for item in re.finditer(regex_url, element):
            element = regex_url.sub('>url', element)
        clean_test.append(element)

    print('Cleaned.')

    print('Vectorizing...')
    vect = TfidfVectorizer(tokenizer=casual_tokenize, max_df=0.8)
    vect.fit(clean_train)
    vect.fit_transform(clean_dev)
    vect.fit_transform(clean_test)
    train_matrix = vect.transform(clean_train)
    dev_matrix = vect.transform(clean_dev)
    test_matrix = vect.transform(clean_test)
    print('Vectorized.')

    return train_matrix.toarray(), dev_matrix.toarray(), test_matrix.toarray()

# Training
def train(train_matrix, train_target):
    #sentiment_classifier = svm.SVC(C=1 ,kernel='linear')
    sentiment_classifier = svm.LinearSVC(C=100, tol=0.01, loss='hinge', max_iter=1000000000)
    #sentiment_classifier = GaussianNB()
    #sentiment_classifier = GradientBoostingClassifier(n_estimators=1000, learning_rate=0.1, max_depth = 3, random_state = 0)
    #sentiment_classifier = SGDClassifier()

    #sentiment_classifier = neighbors.KNeighborsClassifier()
    
    sentiment_classifier.fit(train_matrix, train_target)

    return sentiment_classifier

# Prediction
def predict(matrix, model):
    prediction = model.predict(matrix)

    return prediction

def to_out(ids, tags):
    with open('out.txt', 'a') as file:

        for i in range(len(ids)):
            id = ids[i].split('\n')
            tag = tags[i].split('\n')
            file.write(id[0]+'\t'+tag[0]+'\n')



if __name__ == '__main__':

    print('Loading data...')
    train_text, train_target, dev_text, dev_target, test_text, test_id = load()
    print('Data loaded.')

    print('Preprocessing text...')
    train_matrix, dev_matrix, test_matrix = preprocess(train_text, dev_text, test_text)
    print('Text preprocessed.')

    print('Training model...')
    model = train(train_matrix, train_target)
    print('Model trained.')

    print('Making predictions...')
    out = predict(dev_matrix, model)
    print('Finished.')

    print("accuracy = ", accuracy_score(dev_target, out))
    print("macro = ", precision_recall_fscore_support(dev_target, out, average='macro'))
    print("micro = ", precision_recall_fscore_support(dev_target, out, average='micro'))


    test_out = predict(test_matrix, model)

    to_out(test_id, test_out)
