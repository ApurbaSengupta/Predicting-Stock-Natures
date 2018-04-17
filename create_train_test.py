import random
import json


def clean_data():
    all_data = []
    parsed_data = []
    with open("data/labeled_data.json", "r") as f:
        all_data = json.load(f)

    for article in all_data:
        text = article['article']
        words = text.split(" ")
        if len(words) >= 100:
            parsed_data.append(article)
    return parsed_data


def create_train_test(parsed_data):
    num_points = len(parsed_data)
    data_points = set(random.sample(range(num_points), 100))
    test_data = [parsed_data[i] for i in range(num_points) if i in data_points]
    train_data = [parsed_data[i] for i in range(num_points) if i not in data_points]

    with open("data/train_data.json", "w") as f:
        json.dump(train_data, f)

    with open("data/test_data.json", "w") as f:
        json.dump(test_data, f)


if __name__ == "__main__":
    create_train_test(clean_data())
