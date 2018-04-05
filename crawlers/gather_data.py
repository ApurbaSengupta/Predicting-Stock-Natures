from urllib.request import urlopen
from urllib.parse import urlencode
from newspaper import Article
import pickle
import json
import time
import os

def parse_article(article, data_store, seen_urls):
    article_url = article["url"]
    if article_url not in seen_urls:
        print("Downloading: " + article_url)
        print("")
        news_article = Article(article_url)
        try:
            news_article.download()
            news_article.parse()

            text = news_article.text
            parsed_text = " ".join(text.split("\n"))

            data_store["article"] = parsed_text
            data_store["url"] = article_url
            data_store["host"] = article["source"]["id"]
            seen_urls.add(article_url);
        except:
            print("could not parse article")


def fetch_data_symbol(query, data_store, stock, source, seen_urls):
    url = "https://newsapi.org/v2/everything"
    data = {
        "sources":source,
        "q":query,
        "from":"2017-01-01",
        "language":"en",
        "apiKey":"1b0a021f33f94ebb8afb9ca35defd0eb"
    }
    encoded_data = urlencode(data)
    try:
        contents = json.loads(urlopen(url + "?" + encoded_data).read().decode("utf-8"))
        articles = contents["articles"]

        if len(articles) != 0:
            data_store[stock] = []

        for article in articles:
            article_data = {}
            article_data["date"] = article["publishedAt"]
            parse_article(article, article_data, seen_urls)
            if "article" in article_data:
                data_store[stock].append(article_data)
    except:
        print("ERROR IN CONTACTING NEWS API")


def get_seen_urls():
    if os.path.isfile("seen_urls.pickle"):
        return pickle.load(open("seen_urls.pickle", "rb"));
    else:
        return set()


def get_all_articles():
    if os.path.isfile("../data_store.json"):
        return json.load(open("../data_store.json"))
    else:
        return {}


if __name__ == "__main__":
    all_articles = get_all_articles()
    stock_to_query = {}
    seen_urls = get_seen_urls()
    stock_to_query["AAPL"] = "(Apple Inc OR Apple) NOT Apples"
    stock_to_query["MSFT"] = "MSFT or Microsoft"
    stock_to_query["GOOGL"] = "GOOGL or Google"
    stock_to_query["FB"] = "facebook"
    sources = ["reuters", "bloomberg", "business-insider", "techcrunch", "the-new-york-times"]

    for stock in stock_to_query.keys():
        for source in sources:
            print("Fetching data for: " + stock + ", source = " + source)
            fetch_data_symbol(stock_to_query[stock], all_articles, stock, source, seen_urls)
            time.sleep(3)
            print("==============================================")

    with open("../data_store.json", "w") as f:
        json.dump(all_articles, f)

    with open("seen_urls.pickle", "wb") as f:
        pickle.dump(seen_urls, f)