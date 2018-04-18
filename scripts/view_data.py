import json

def print_data(label, filename):
    with open(filename, "r") as f:
        data = json.load(f)
        data_parsed = [x for x in data if int(x['label']) == label][:100]
        for item in data_parsed:
            #print(item.keys())
            print(item['article'])
            print("STOCK: ", item['stock'])
            print("SOURCE: ", item['source'])
            print("URL: ", item['url'])
            print("LABEL: ", item['label'])
            print("====================================")


train_data = "../data/train_data.json"
test_data = "../data/test_data.json"
print_data(1, test_data)