from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from parse_data import *
import sys


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

X, y = get_sentiment_adj_data(w2v, train_data, dim)
#print("sample doc vector", X[0])

print("data gathered")

X_test, y_test = get_sentiment_adj_data(w2v, test_data, dim)

print("proceeding to fit SVM...")

print("num training data: ", len(X))
print("num labels: ", len(y))

clf = SVC(kernel='linear')
clf.fit(X, y)
print("SVM fitted!")

y_pred = clf.predict(X_test)
print("Classification Accuracy: ", accuracy_score(y_test, y_pred))
