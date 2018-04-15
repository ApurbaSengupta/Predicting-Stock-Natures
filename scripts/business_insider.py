from newspaper import Article
import requests
import json

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

#url = "https://www.businessinsider.com/electric-cars-challenging-tesla-model-3-2018-1"
url = "https://www.businessinsider.com/facebook-stock-price-rallies-ahead-of-earnings-2018-1"
#url = "https://www.businessinsider.com/apple-making-over-ear-headphones-2018-2"
# URL TO LOOK INTO: https://www.nytimes.com/2018/02/26/opinion/united-states-searching-data-overseas.html

cookies = {"__pnahc": "0"}
r = requests.get(url, cookies=cookies)

article = Article('')
article.download(input_html=r.text)
article.parse()

text = article.text
parsed_text = " ".join(text.split("\n"))

print(parsed_text)

#print(r.text)