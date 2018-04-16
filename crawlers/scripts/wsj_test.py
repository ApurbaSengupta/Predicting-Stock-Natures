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

#url = "https://www.wsj.com/articles/microsoft-reports-gains-in-cloud-computing-business-1517434433"
url = "https://blogs.wsj.com/moneybeat/2018/04/02/some-good-news-for-tesla/"

cookies = get_cookies("wsj_cookies.txt")
print("USER BKT: " + cookies["usr_bkt"])
r = requests.get(url, cookies=cookies)

article = Article('')
article.download(input_html=r.text)
article.parse()

text = article.text
parsed_text = " ".join(text.split("\n"))

print(parsed_text)

#print(r.text)