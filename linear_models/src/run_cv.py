from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import accuracy_score
from parse_data import *


def run_naive_bayes(c, train_data, test_data):
    X, y, tfidf = get_tfidf_data(train_data)

    X_test, y_test, tfidf = get_tfidf_data(test_data, tfidf=tfidf)
    clf = BernoulliNB(alpha=c)
    clf.fit(X, y)

    y_pred = clf.predict(X_test)
    acc_score = accuracy_score(y_test, y_pred)
    print("Accuracy: ", acc_score)
    return acc_score


# function that returns testing accuracy of tfidf
def run_log_regression(c, train_data, test_data):
    X, y, tfidf = get_tfidf_data(train_data)

    X_test, y_test, tfidf = get_tfidf_data(test_data, tfidf=tfidf)
    clf = LogisticRegression(C=c)
    clf.fit(X, y)

    y_pred = clf.predict(X_test)
    acc_score = accuracy_score(y_test, y_pred)
    print("Accuracy: ", acc_score)
    return acc_score


# function that returns testing accuracy of
# svm with tfidf vectors, for given regularization and
# training/testing fold
def run_tfidf(c, train_data, test_data):
    X, y, tfidf = get_tfidf_data(train_data)

    X_test, y_test, tfidf = get_tfidf_data(test_data, tfidf=tfidf)

    clf = SVC(C=c, kernel='linear')
    clf.fit(X, y)

    y_pred = clf.predict(X_test)
    acc_score = accuracy_score(y_test, y_pred)
    print("Accuracy: ", acc_score)
    return acc_score


cv_folder = "../oracle/data/cv/fold"
reg_vals = [1, 0.9, 0.8, 0.7, 0.6, 0.5]

lst_testing_acc = []

for c_val in reg_vals:
    fold_vals = []
    for i in range(5):
        train_path = cv_folder + str(i) + "/train_data.json"
        test_path = cv_folder + str(i) + "/test_data.json"
        print("Fold %i, C Val: %f" % (i, c_val))
        #fold_vals.append(run_tfidf(c_val, train_path, test_path))
        #fold_vals.append(run_log_regression(c_val, train_path, test_path))
        fold_vals.append(run_naive_bayes(c_val, train_path, test_path))
        print("=================================")
    mean_acc = sum(fold_vals)*1.0 / len(fold_vals)
    lst_testing_acc.append(mean_acc)

largest_acc = max(lst_testing_acc)
inx = lst_testing_acc.index(largest_acc)
print("Optimal C: ", reg_vals[inx])
print("Largest Accuracy: ", largest_acc)
