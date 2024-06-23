import yfinance as yf
import urllib.request
import json


def get_name(ticker):

    stock_name = yf.Ticker(ticker).info["longName"]

    return stock_name


# def get_yahoo_shortname(symbol):
#     response = urllib.request.urlopen(
#         f"https://query2.finance.yahoo.com/v1/finance/search?q={symbol}"
#     )
#     content = response.read()
#     data = json.loads(content.decode("utf8"))["quotes"][0]["shortname"]
#     return data


name = get_name("AAPL")
print(name)
name = get_name("AMD")
print(name)
name = get_name("NVDA")
print(name)
