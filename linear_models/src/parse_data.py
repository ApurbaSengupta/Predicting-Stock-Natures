from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk import word_tokenize
import numpy as np
import pickle
import json


def get_50_w2v():
    with open("glove_files/50.pickle", "rb") as f:
        return pickle.load(f)


def get_100_w2v():
    with open("glove_files/100.pickle", "rb") as f:
        return pickle.load(f)


def get_200_w2v():
    with open("glove_files/200.pickle", "rb") as f:
        return pickle.load(f)


def get_300_w2v():
    with open("glove_files/300.pickle", "rb") as f:
        return pickle.load(f)


def get_mock_w2v():
    return {"word1": [1.0, 2.0, 3.0], "word2": [1.0, 2.0, 3.0],
            "word3": [3.4, 5.6, 7.8]}


# function to return of list words from article
# stop words are removed
def parse_text(article):
    tokens = word_tokenize(article)
    lower_tokens = [x.lower() for x in tokens]
    stops = set(stopwords.words('english'))

    return [x for x in tokens if x.lower() not in stops]

    #return [x for x in lower_tokens if x not in stops]


def get_tfidf_vector(text, tfidf):
    mat = tfidf.transform([text])
    return mat.toarray()[0]


def get_tfidf_token_vec(article, word_to_inx, tfidf):
    mat = tfidf.transform([article])
    vec = mat.toarray()[0]
    tokens = parse_text(article)
    return [vec[word_to_inx[token]] if token in word_to_inx else 0 for token in tokens]


def get_sentiment_words():
    pos_words = set()
    neg_words = set()

    with open("pos_words_set.pickle", "rb") as f:
        pos_words = pickle.load(f)

    with open("neg_words_set.pickle", "rb") as f:
        neg_words = pickle.load(f)

    return pos_words, neg_words


# function averages word vectors for all words in article
def normalize_word_vecs(tokens, w2v, dim, pos_words=None, neg_words=None, tf_idf=None):
    if pos_words is None or neg_words is None:
        return np.mean([w2v[word] if word in w2v else np.zeros(dim) for word in tokens], axis=0)
    else:
        coeff_pos_words = np.array([500 if x in pos_words else 0 for x in tokens])
        coeff_neg_words = np.array([-500 if x in neg_words else 0 for x in tokens])
        other_words = np.array([1 if (x not in pos_words and x not in neg_words)
                                else 0 for x in tokens])
        coeff = coeff_pos_words + coeff_neg_words + other_words

        if tf_idf is not None:
            coeff = coeff * tf_idf

        total = np.array([w2v[word] if word in w2v else np.zeros(dim) for word in tokens]) * \
                coeff[:, None]
        mean = np.mean(total, axis=0)
        return mean


# function that returns vectorized data of given train/test file (without any sentiment adjusted
# data)
def get_data(w2v, filename, dim):
    with open(filename, "r") as f:
        data = json.load(f)
        all_tokens = [parse_text(x['article']) for x in data]
        all_labels = [int(x['label']) for x in data]
        vectorized_data = np.array([normalize_word_vecs(x, w2v, dim) for x in all_tokens])
        return vectorized_data, all_labels


# function that returns vectorized data, adjusting for sentiment information
def get_sentiment_adj_data(w2v, filename, dim):
    pos_words, neg_words = get_sentiment_words()
    with open(filename, "r") as f:
        data = json.load(f)
        all_tokens = [parse_text(x['article']) for x in data]
        all_labels = [int(x['label']) for x in data]
        vectorized_data = np.array([normalize_word_vecs(x, w2v, dim, pos_words=pos_words,
                                                        neg_words=neg_words) for x in all_tokens])
        return vectorized_data, all_labels


# return tf-idf vectors for each document
def get_tfidf_data(filename, tfidf=None):
    with open(filename, "r") as f:
        data = json.load(f)
        all_text = [x['article'] for x in data]
        all_labels = [int(x['label']) for x in data]
        if tfidf is None:
            tfidf = TfidfVectorizer(tokenizer=word_tokenize, stop_words=stopwords.words('english'))
            tfidf.fit(all_text)

        vectorized_data = np.array([get_tfidf_vector(text, tfidf) for text in all_text])

        return vectorized_data, all_labels, tfidf


def get_tfidf_ngram_data(filename, ngram, tfidf=None):
    with open(filename, "r") as f:
        data = json.load(f)
        all_text = [x['article'] for x in data]
        all_labels = [int(x['label']) for x in data]
        if tfidf is None:
            tfidf = TfidfVectorizer(tokenizer=word_tokenize, stop_words=stopwords.words('english'),
                                    ngram_range=(1, ngram))
            tfidf.fit(all_text)

        vectorized_data = np.array([get_tfidf_vector(text, tfidf) for text in all_text])

        return vectorized_data, all_labels, tfidf


# return vectors that are weighted by sentiment as well as tf-idf values
def get_tfidf_sentiment_data(w2v, filename, dim, tfidf=None):
    pos_words, neg_words = get_sentiment_words()
    with open(filename, "r") as f:
        data = json.load(f)
        all_text = [x['article'].lower() for x in data]
        all_labels = [int(x['label']) for x in data]

        if tfidf is None:
            tfidf = TfidfVectorizer(tokenizer=word_tokenize, stop_words=stopwords.words('english'))
            tfidf.fit(all_text)

        feature_names = tfidf.get_feature_names()
        word_to_inx = {v: k for k, v in feature_names.items()}

        vectorized_data = np.array([normalize_word_vecs(parse_text(x), w2v, dim,
                                                        pos_words=pos_words, neg_words=neg_words,
                                                        tf_idf=get_tfidf_token_vec(x, word_to_inx, tfidf)
                                                        ) for x in all_text])
        return vectorized_data, all_labels, tfidf




