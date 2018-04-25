from hashlib import md5
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


# function serves to handle lack of content-seen test
# in crawling. Multiple urls may end up having the same
# article content. Thus we hash articles here and only
# add articles not in set of pre-computed hashes
def remove_duplicate_data(parsed_data):
    dup_removed_data = []
    seen_content = set()
    for article in parsed_data:
        text = article['article'].strip()
        text_hash = md5(text.encode()).hexdigest()
        if text_hash not in seen_content:
            seen_content.add(text_hash)
            dup_removed_data.append(article)
    return dup_removed_data



def create_train_test(parsed_data):
    num_points = len(parsed_data)
    data_points = set(random.sample(range(num_points), 100))
    test_data = [parsed_data[i] for i in range(num_points) if i in data_points]
    train_data = [parsed_data[i] for i in range(num_points) if i not in data_points]

    with open("data/train_data2.json", "w") as f:
        json.dump(train_data, f)

    with open("data/test_data2.json", "w") as f:
        json.dump(test_data, f)

    with open("data/labeled_data2.json", "w") as f:
        json.dump(parsed_data, f)


if __name__ == "__main__":
    create_train_test(remove_duplicate_data(clean_data()))
