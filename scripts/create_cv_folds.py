import json


def get_data():
    with open("data/labeled_data.json", "r") as f:
        all_data = json.load(f)
        return all_data


def create_cv_folds():
    data = get_data()
    num_elements = int(len(data) / 5)
    parititons = []
    for i in range(0, len(data), num_elements):
        parititons.append(data[i:i+num_elements])

    parititons[4] = parititons[4] + parititons[5]
    parititons = parititons[:5]

    for i in range(5):
        root_path = "data/cv/fold" + str(i) + "/"
        train_path = root_path + "train_data.json"
        test_path = root_path + "test_data.json"

        test_data = parititons[i];
        train_data_comp = [parititons[j] for j in range(5) if j != i]
        train_data = [item for sublist in train_data_comp for item in sublist]
        with open(train_path, "w") as f, open(test_path, "w") as f2:
            json.dump(train_data, f)
            json.dump(test_data, f2)    


create_cv_folds()