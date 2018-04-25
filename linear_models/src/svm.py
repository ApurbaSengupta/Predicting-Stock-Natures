from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from parse_data import get_data, get_100_w2v


train_data = "../oracle/data/train_data.json"
test_data = "../oracle/data/test_data.json"

w2v = get_100_w2v()
print("Word Embeddings loaded into memory")

X, y = get_data(w2v, train_data, 100)
print("data gathered")

X_test, y_test = get_data(w2v, test_data, 100)

print("proceeding to fit SVM...")
clf = SVC(kernel='linear')
clf.fit(X, y)
print("SVM fitted!")

y_pred = clf.predict(X_test)
print("Classification Accuracy: ", accuracy_score(y_test, y_pred))
