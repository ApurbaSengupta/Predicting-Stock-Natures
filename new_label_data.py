from datetime import date, timedelta
import json
import csv
import numpy as np

class StockData:
    # class to hold stock information
    def __init__(self, open_price, close_price, date, stock):
        self.open = open_price
        self.close = close_price
        self.date = date
        self.stock = stock

    def get_open_price(self):
        return self.open

    def get_close_price(self):
        return self.close

    def get_date(self):
        return self.date

    def get_stock(self):
        return self.stock


def parse_date(date_str, delim):
    arr = date_str.split(delim)
    dt = date(int(arr[0]), int(arr[1]), int(arr[2]));
    return dt


def is_weekend(dt):
    return dt.isoweekday in set([6, 7])


def get_prev_market_day(dt, price_data):
    new_dt = dt
    while new_dt.isoformat() not in price_data:
        new_dt = new_dt - timedelta(days=1)
    return new_dt


def get_next_market_day(dt, price_data):
    new_dt = dt
    last_date = date(2018, 4, 13)
    while new_dt.isoformat() not in price_data:
        new_dt = new_dt + timedelta(days=1)
        if new_dt > last_date:
            return None
    return new_dt


# helper function to get the next closest market day
# a day could be either a weekend, or a holiday
def get_market_day(dt, price_data, window=-1):
    if window == -1:
        if dt.isoformat() not in price_data:
            return get_prev_market_day(dt, price_data)
        return dt
    else:
        new_dt = dt + timedelta(days=window)
        if new_dt.isoformat() not in price_data:
            return get_next_market_day(new_dt, price_data)
        return new_dt



def get_price_data(data_file):
    price_data = {}

    with open(data_file, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            parsed_date = parse_date(row['datadate'], "/").isoformat()
            open_price = float(row['prcod'])
            close_price = float(row['prccd'])
            ticker = row['tic']

            stock = StockData(open_price, close_price, parsed_date, ticker)
            if parsed_date in price_data:
                price_data[parsed_date][ticker] = stock
            else:
                price_data[parsed_date] = {ticker: stock}
    return price_data


def get_labeled_data(price_data, data_store, window):
    grouped_data = {}
    all_data = []
    delt = timedelta(days=window)

    stocks_to_get_data = set(["PYPL"])
    source_to_consider = set(["reuters", "bloomberg", "business-insider", "the-new-york-times", 
        "financial-times", "the-wall-street-journal"])
    curr_stocks = [x for x in data_store if x not in stocks_to_get_data]
    #print(curr_stocks)
    for stock in curr_stocks:
        grouped_data[stock] = []
        for article in data_store[stock]:
            if article['host'] in source_to_consider:
                article_date = article['date'].split("T")[0]
                article_date_obj = parse_date(article_date, "-")
                init_week_date = get_market_day(article_date_obj, price_data).isoformat()
                init_price = price_data[init_week_date][stock].get_open_price()

                fin_date = get_market_day(article_date_obj, price_data, 2)
                if fin_date == None:
                    continue

                fin_price = price_data[fin_date.isoformat()][stock].get_close_price()
                if np.log(fin_price) - np.log(init_price) > 0.0031:
                    article["label"] = 1
                elif np.log(fin_price) - np.log(init_price) < -0.0045:
                    article["label"] = -1    
                else:
                    article["label"] = 0
                grouped_data[stock].append(article)
                all_data.append({"article": article['article'], "stock": stock, "label": article['label'], 
                "date": article_date, "source": article['host'], "url": article['url']})
    return grouped_data, all_data


if __name__ == "__main__":
    data_file = "stock_data/stock_price_data.csv"
    articles = "data_store.json"
    data_store = {}

    with open(articles, "r") as f:
        data_store = json.load(f)

    price_data = get_price_data(data_file)

    grouped_data, all_data = get_labeled_data(price_data, data_store, 2)

    with open("grouped_data.json", "w") as f:
        json.dump(grouped_data, f)

    with open("labeled_data.json", "w") as f:
        json.dump(all_data, f)