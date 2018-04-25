from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from gensim.utils import simple_preprocess
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import accuracy_score
from nltk import word_tokenize, sent_tokenize
import random
import pickle
import json

'''
best results: vector_size = 100, num_epochs = 5, window=None

'''

def get_list_tagged_docs(trainfile):
    docs = []
    with open(trainfile, "r") as f:
        all_articles = json.load(f)
        i = 0
        for article in all_articles:
            text = article['article']
            words = simple_preprocess(text)
            label = "label_" + str(i)
            docs.append(TaggedDocument(words, label))
            i += 1
    return docs


def get_list_docs(filename):
    with open(filename, "r") as f:
        data = json.load(f)
        articles = [simple_preprocess(x['article']) for x in data]
        labels = [int(x['label']) for x in data]
        return articles, labels


def get_sentiment_words():
    pos_words = set()
    neg_words = set()

    with open("pos_words_set.pickle", "rb") as f:
        pos_words = pickle.load(f)

    with open("neg_words_set.pickle", "rb") as f:
        neg_words = pickle.load(f)

    return pos_words, neg_words


def train_model(documents, train_docs, test_docs, num_epochs):
    print("Building Doc2Vec Model")
    model = Doc2Vec(alpha=0.025, min_alpha=0.025, vector_size=100, min_count=3)
    model.build_vocab(documents)

    print("Number of Epochs: ", num_epochs)
    print("Number of documents: ", model.corpus_count)

    for epoch in range(num_epochs):
        print("Training epoch: %i" % epoch)
        random.shuffle(documents)
        model.train(documents, total_examples=model.corpus_count, epochs=1)
        model.alpha -= 0.002
        model.min_alpha = model.alpha

    # model.train(documents, total_examples=model.corpus_count, epochs=num_epochs)

    X_train = [model.infer_vector(x) for x in train_docs]
    X_test = [model.infer_vector(x) for x in test_docs]

    return X_train, X_test

train_data = "../oracle/data/train_data.json"
test_data = "../oracle/data/test_data.json"

docs = get_list_tagged_docs(train_data)
docs_test, y_test = get_list_docs(test_data)
docs_train, y = get_list_docs(train_data)

X_train, X_test = train_model(docs, docs_train, docs_test, 20)
#print("Trained Vectors: ", X_train)

# clf = SVC(kernel='linear')
# clf = LogisticRegression(C=1)
clf = BernoulliNB(alpha=0.6)
print("Svm Fitted!")
clf.fit(X_train, y)

y_pred = clf.predict(X_test)
print("Testing Accuracy: ", accuracy_score(y_test, y_pred))
