from urllib.request import urlopen
from urllib.parse import urlencode
from newspaper import Article
import requests
import pickle
import json
import time
import os

def parse_article(article, article_data, seen_urls, cookies):
    article_url = article["url"]
    if article_url not in seen_urls:
        print("Downloading: " + article_url)
        print("")

        article_data["url"] = article_url
        article_data["host"] = article["source"]["id"]

        try:
            parsed_text = ""
            # download article normally if no cookies are needed
            if len(cookies) == 0:
                news_article = Article(article_url)
                news_article.download()
                news_article.parse()
                text = news_article.text
                parsed_text = " ".join(text.split("\n"))
            else:
                # download article with cookies if needed
                print("parsing requests with cookies")
                r = requests.get(article_url, cookies=cookies)
                news_article = Article("")
                news_article.download(input_html=r.text)
                news_article.parse()
                text = news_article.text
                parsed_text = " ".join(text.split("\n"))

            article_data["article"] = parsed_text
            seen_urls.add(article_url);
        except:
            print("could not parse article")


def fetch_data_symbol(query, data_store, stock, source, cookies, seen_urls):
    url = "https://newsapi.org/v2/everything"
    data = {
        "sources":source,
        "q":query,
        "from":"2017-01-01",
        "language":"en",
        "apiKey":"eb3a4219f13a4ddaa7d5b9f82c6df28a"
    }
    #encoded_data = urlencode(data)
    try:
    #contents = json.loads(urlopen(url + "?" + encoded_data).read().decode("utf-8"))
        r = requests.get(url, params=data)
        contents = json.loads(r.text)
        #print(r.text)
        articles = contents["articles"]

    # initialize the array of articles for new stock
        if len(articles) != 0 and (stock not in data_store):
            data_store[stock] = []

    # add articles to data_store
        for article in articles:
            article_data = {}
            article_data["date"] = article["publishedAt"]
            parse_article(article, article_data, seen_urls, cookies)

            # only add articles that could be downloaded and parsed
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

def get_cookies(cookie_file):
    cookies = {}

    with open(cookie_file, "r") as f:
        line = f.readline()
        tokens = line.split(";")
        for token in tokens:
            parts = token.split("=")
            key = parts[0].strip()
            val = parts[1].strip()
            cookies[key] = val

    return cookies

if __name__ == "__main__":

    # Initialize data structures to collect article information
    all_articles = get_all_articles()
    stock_to_query = {}
    seen_urls = get_seen_urls()

    # correlate stock ticker to search query
    stock_to_query["AAPL"] = "(Apple Inc OR Apple OR apple) NOT (Apples OR apples)"
    stock_to_query["MSFT"] = "Microsoft OR Microsoft Corporation OR microsoft"
    stock_to_query["GOOGL"] = "google OR Google"
    stock_to_query["FB"] = "Facebook OR facebook"
    stock_to_query["PYPL"] = "PayPal OR Paypal OR paypal"
    stock_to_query["TSLA"] = "Tesla OR tesla"
    stock_to_query["AMZN"] = "(AMZN OR Amazon OR amazon) NOT (forest)"
    stock_to_query["IBM"] = "IBM OR ibm"
    stock_to_query["INTC"] = "INTC OR Intel"
    stock_to_query["NFLX"] = "Netflix OR netflix OR NFLX"
    stock_to_query["NVDA"] = "NVDA OR Nvdia OR nvidia"
    stock_to_query["BABA"] = "BABA OR Alibaba OR alibaba"

    # initialize sources and cookies for some sources
    sources = ["reuters", "bloomberg", "business-insider", "techcrunch", "the-new-york-times", 
    "techradar", "financial-times", "engadget", "the-wall-street-journal"]

    cookie_data = {}
    cookie_data["the-wall-street-journal"] = get_cookies("wsj_cookies.txt")
    cookie_data["business-insider"] = {"__pnahc": "0"}

    for stock in stock_to_query:
        for source in sources:
            print("Fetching data for: " + stock + ", source = " + source)

            cookies = {}
            if source in cookie_data:
                cookies = cookie_data[source]

            fetch_data_symbol(stock_to_query[stock], all_articles, stock, source, cookies, seen_urls)
            #time.sleep(3)
            print("==============================================")

    with open("../data_store.json", "w") as f:
        json.dump(all_articles, f)

    with open("seen_urls.pickle", "wb") as f:
        pickle.dump(seen_urls, f)