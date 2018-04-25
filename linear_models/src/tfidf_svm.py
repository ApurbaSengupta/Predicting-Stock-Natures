from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from parse_data import *

train_data = "../oracle/data/train_data.json"
test_data = "../oracle/data/test_data.json"

# X, y, tfidf = get_tfidf_data(train_data)
X, y, tfidf = get_tfidf_ngram_data(train_data, 2)

# X_test, y_test, tfidf = get_tfidf_data(test_data, tfidf=tfidf)
X_test, y_test, tfidf = get_tfidf_ngram_data(test_data, 2, tfidf=tfidf)

clf = SVC(C=0.8, kernel='linear')
clf.fit(X, y)

y_pred = clf.predict(X_test)
print("Testing Accuracy: ", accuracy_score(y_test, y_pred))
y_pred_train = clf.predict(X)
print("Training Accuracy: ", accuracy_score(y, y_pred_train))
