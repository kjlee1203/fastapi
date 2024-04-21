import requests
from pprint import pprint
import sys


# Store the current standard output (usually the console)
original_stdout = sys.stdout

# Open a text file in write mode
with open("output.txt", "w") as f:
    # Redirect standard output to the text file
    sys.stdout = f

    url = "https://api.upbit.com/v1/candles/days"

    headers = {"accept": "application/json"}
    data = []
    for ticker in ["KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-ADA", "KRW-DOGE"]:
        # for ticker in ["KRW-BTC", "KRW-DOGE"]:

        params = {
            "market": ticker,
            "to": "2023-10-04 00:00:00",
            "count": 200,
            "convertingPriceUnit": "KRW",
        }

        response = requests.get(url, headers=headers, params=params)
        data.extend(response.json())
    pprint(data)

with open("data2.txt", "w") as f:
    # Redirect standard output to the text file
    sys.stdout = f

    # Print a message to the console indicating that the output has been saved
    modified_data = [
        {
            "date": item["candle_date_time_kst"][:10],
            "open": item["opening_price"],
            "high": item["high_price"],
            "low": item["low_price"],
            "close": item["trade_price"],
            "volume": item["candle_acc_trade_volume"],
            "ticker": item["market"],
        }
        for item in data
    ]

    pprint(modified_data)
