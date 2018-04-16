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


if __name__ == "__main__":
    check_labeled_data()
