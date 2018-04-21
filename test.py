import nltk
import json
import sys

def check_data_store():
    data_store = {}
    with open("data_store.json", "r") as f:
        data_store = json.load(f)

    sum = 0;
    for key in data_store:
        print(key + ": " + str(len(data_store[key])))
        sum += len(data_store[key])

    print("Total Articles: " + str(sum))


def check_labeled_data():
    labeled_data = []
    with open("data/labeled_data.json", "r") as f:
        labeled_data = json.load(f)

    for article in labeled_data:
        print(article['article'])
        print("---------------------------------")
        print("Stock: " + article['stock'])
        print("Source: " + article['source'])
        print("Label: " + str(article['label']))
        print("========================================================================")


def print_sents():
    with open("data/train_data.json", "r") as f:
        data = json.load(f)
        article = data[1];
        text = article['article']
        sentences = nltk.sent_tokenize(text)
        for sent in sentences:
            print(sent)



if __name__ == "__main__":
    print_sents()
