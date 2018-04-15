import json
import sys

data_store = {}
with open("data_store.json", "r") as f:
    data_store = json.load(f)

sum = 0;
for key in data_store:
    print(key + ": " + str(len(data_store[key])))
    sum += len(data_store[key])

print("Total Articles: " + str(sum))
