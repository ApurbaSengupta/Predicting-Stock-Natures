import json

data_store = {}
with open("data_store.json", "r") as f:
    data_store = json.load(f);

arr = data_store["AAPL"]
for i in range(len(arr)):
    print(arr[i]["url"])
    print(arr[i]["article"])
    print("=========================")