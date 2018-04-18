from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from parse_data import *
import sys

train_data = "../oracle/data/train_data.json"
test_data = "../oracle/data/test_data.json"

X, y, tfidf = get_tfidf_data(train_data)
print("parsed training data")

X_test, y_test, tfidf = get_tfidf_data(train_data, tfidf=tfidf)
print("parsed testing data")

clf = SVC(kernel='linear')
clf.fit(X, y)
print("svm fitted!")

y_pred = clf.predict(X_test)
print("Classification Accuracy: ", accuracy_score(y_test, y_pred))
