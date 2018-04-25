from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import sys
from parse_data import *


train_data = "../oracle/data/train_data.json"
test_data = "../oracle/data/test_data.json"


dim = int(sys.argv[1])
w2v = None

if dim == 50:
    w2v = get_50_w2v()
elif dim == 100:
    w2v = get_100_w2v()
elif dim == 200:
    w2v = get_200_w2v()
elif dim == 300:
    w2v = get_300_w2v()
else:
    w2v = get_mock_w2v()

print("Word Embeddings loaded into memory")


#X, y, tfidf = get_tfidf_data(train_data)
# X, y, tfidf = get_tfidf_ngram_data(train_data, 2)
X, y = get_sentiment_adj_data(w2v, train_data, dim)

X_test, y_test = get_sentiment_adj_data(w2v, test_data, dim)
# X_test, y_test, tfidf = get_tfidf_data(test_data, tfidf=tfidf)
# X_test, y_test, tfidf = get_tfidf_ngram_data(test_data, 2, tfidf=tfidf)

clf = LogisticRegression(C=1)
clf.fit(X, y)

y_pred = clf.predict(X_test)
print("Testing Accuracy: ", accuracy_score(y_test, y_pred))
y_pred_train = clf.predict(X)
print("Training Accuracy: ", accuracy_score(y, y_pred_train))
