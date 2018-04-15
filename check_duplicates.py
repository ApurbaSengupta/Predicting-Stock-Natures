import json
import sys

data_store = {}
with open("data_store.json", "r") as f:
    data_store = json.load(f)

stock = sys.argv[1]
all_articles = data_store[stock]

group_host = {}

for article in all_articles:
    host = article["host"]
    if host in group_host:
        group_host[host].append(article);
    else:
        group_host[host] = [article]

host = "business-insider"
for article in group_host[host]:
    print(article["url"])
    print(article["article"])
    print("===========================")

'''for host in group_host:
    print("HOST: " + host)
    for wsj_article in group_host[host]:
    #print("HOST: " + host)
    #print("DATE: " + article["date"])
        print("URL: " + article["url"])
    #print(article["article"]);
    print(str(len(group_host[host])))
    print("===========================")'''


#for host, article in lst_articles:
#    print("HOST: " + host)
#    print("DATE: " + article["date"])
#    print("URL: " + article["url"])
#    print(article["article"]);
#    print("===========================")