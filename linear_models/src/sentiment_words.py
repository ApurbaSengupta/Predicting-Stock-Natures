from nltk import word_tokenize
from scipy.stats import pearsonr
import pickle
import json


def get_labeled_data():
    with open("../oracle/data/labeled_data.json") as f:
        return json.load(f)


def get_all_words(all_data):
    lst_words = [word_tokenize(x['article']) for x in all_data]
    return set([item.lower() for sublist in lst_words for item in sublist])


def get_positive_words():
    with open("../positive-words.txt", "r") as f:
        return set([line.strip() for line in f.readlines()])


def get_negative_words():
    with open("../negative-words.txt", "r") as f:
        return set([line.strip() for line in f.readlines()])


def pickle_sentiment_words():
    data = get_labeled_data()
    all_words = get_all_words(data)
    positive_words = get_positive_words()
    negative_words = get_negative_words()

    pos_words_data = all_words.intersection(positive_words)
    neg_words_data = all_words.intersection(negative_words)

    with open("pos_words_set.pickle", "wb") as f:
        pickle.dump(pos_words_data, f)

    with open("neg_words_set.pickle", "wb") as f:
        pickle.dump(neg_words_data, f)


def count_intersection(set_words, article):
    article_set = set(article)
    return len(set_words.intersection(article_set))


def check_num_sentiment_words():
    pos_words = get_positive_words()
    neg_words = get_negative_words()

    train_data = "../oracle/data/train_data.json"
    test_data = "../oracle/data/test_data.json"

    with open(train_data, "r") as f, open(test_data, "r") as f2:
        train = json.load(f)
        test = json.load(f2)

        all_words_train = [word_tokenize(x['article']) for x in train]
        all_words_test = [word_tokenize(x['article']) for x in test]

        num_pos_train = [count_intersection(pos_words, x) for x in all_words_train]
        num_neg_train = [count_intersection(neg_words, x) for x in all_words_train]

        combine_train = list(zip(num_pos_train, num_neg_train))

        num_pos_test = [count_intersection(pos_words, x) for x in all_words_test]
        num_neg_test = [count_intersection(neg_words, x) for x in all_words_test]

        combine_test = list(zip(num_pos_test, num_neg_test))

        print("Max POS: ", max(num_pos_train))
        print("Avg POS: ", sum(num_pos_train) * 1.0 / len(num_pos_train))
        print("Max NEG: ", max(num_neg_train))
        print("Avg NEG: ", sum(num_neg_train) * 1.0 / len(num_neg_train))
        print("====================================")
        print("TEST max pos: ", max(num_pos_test))
        print("Test avg pos: ", sum(num_pos_test) * 1.0 / len(num_pos_test))
        print("TEST max neg: ", max(num_neg_test))
        print("Test avg neg: ", sum(num_neg_test) * 1.0 / len(num_neg_test))
        print("====================================")
        X = [x[0] - x[1] for x in combine_train]
        Y = [x['label'] for x in train]
        print(X)
        print(Y)
        corr = pearsonr(X, Y)
        print("Correlation in train: ", corr)
        '''for i in range(len(combine_train)):
            print(str(combine_train[i]) + ", label: " + str(train[i]['label']))
        print("====================================")
        for i in range(len(combine_test)):
            print(str(combine_test[i]) + ", label: " + str(test[i]['label']))'''


check_num_sentiment_words()


