from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score
from parse_data import *

train_data = "../oracle/data/train_data.json"
test_data = "../oracle/data/test_data.json"

X, y, tfidf = get_tfidf_data(train_data)
# X, y, tfidf = get_tfidf_ngram_data(train_data, 2)

X_test, y_test, tfidf = get_tfidf_data(test_data, tfidf=tfidf)
# X_test, y_test, tfidf = get_tfidf_ngram_data(test_data, 2, tfidf=tfidf)


clf = KMeans(n_clusters=2)
kmeans = clf.fit(X)
i = 0
assigned_labels = kmeans.labels_
for item in assigned_labels:
    print(item, y[i])
    i += 1
