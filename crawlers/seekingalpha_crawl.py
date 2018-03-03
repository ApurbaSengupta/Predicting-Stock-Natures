from newspaper import Article
from lxml import html, etree;
import json

base_url = "https://seekingalpha.com/symbol/%s/analysis-and-news"
stocks = ["NVDA", "MSFT", "AAPL", "GOOG", "AMAZ", "FB"]
all_articles = {}

with open("../output.json", "r") as f:
    all_articles = json.load(f);

for stock in stocks:
    url = base_url % stock
    # TODO: finish