from newspaper import Article
from lxml import html, etree;
import json

# Reading Data from website
base_url = "https://www.reuters.com/finance/stocks/company-news/"
stocks = ["NVDA", "MSFT", "AAPL", "GOOG", "AMAZ", "FB"]
site_url = "https://www.reuters.com";

all_articles = {}

with open("output.json", "r") as f:
    all_articles = json.load(f);

for stock in stocks:
    print("Current Stock: " + stock)
    url = base_url + stock

    if stock not in all_articles:
        all_articles[stock] = []

    article = Article(url)
    article.download()
    tree = html.fromstring(article.html);
    # getting links for news
    links = tree.xpath('//div[@id="companyNews"]/div[@class="module"]/div/div/h2/a/@href')
    
    for link in links:
        article_url = site_url + link
        print("Downloading: " + article_url)
        print("")
        news_article = Article(article_url);
        news_article.download();
        news_article.parse();

        date = news_article.publish_date.strftime("%m/%d/%Y %H:%M:%S");
        text = news_article.text;
        parsed_text = " ".join(text.split("\n"));
        dct = {}
        dct["date"] = date;
        dct["article"] = parsed_text;
        all_articles[stock].append(dct);


# Writing to json file
with open("output.json", "w") as f:
    json.dump(all_articles, f);

