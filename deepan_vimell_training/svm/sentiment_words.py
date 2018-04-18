from nltk import word_tokenize
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


pickle_sentiment_words()


