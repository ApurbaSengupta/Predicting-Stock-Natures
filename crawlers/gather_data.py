from urllib.request import urlopen
from urllib.parse import urlencode
from newspaper import Article
import json

def parse_article(article, data_store):
    article_url = article["url"]
    print("Downloading: " + article_url)
    print("")
    news_article = Article(article_url)
    try:
        news_article.download()
        news_article.parse()

        text = news_article.text
        parsed_text = " ".join(text.split("\n"))

        data_store["article"] = parsed_text
        data_store["url"] = article_url;
        data_store["host"] = article["source"]["id"]
    except:
        print("could not parse article")


def fetch_data_symbol(stock, data_store):
    url = "https://newsapi.org/v2/everything"
    data = {
        "sources":"bloomberg,reuters,the-wall-street-journal,techcrunch",
        "q":stock,
        "language":"en",
        "apiKey":"1b0a021f33f94ebb8afb9ca35defd0eb"
    }
    encoded_data = urlencode(data);
    contents = json.loads(urlopen(url + "?" + encoded_data).read().decode("utf-8"))
    articles = contents["articles"];

    if len(articles) != 0:
        data_store[stock] = []

    for article in articles:
        article_data = {};
        article_data["date"] = article["publishedAt"];
        parse_article(article, article_data)
        if "article" in article_data:
            data_store[stock].append(article_data)


if __name__ == "__main__":
    all_articles = {}
    stocks = ["MSFT", "AAPL", "GOOG"]
    #stocks = ["AAPL"]

    for stock in stocks:
        fetch_data_symbol(stock, all_articles)

    with open("../data_store.json", "w") as f:
        json.dump(all_articles, f)