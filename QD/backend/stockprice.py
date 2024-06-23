import requests
from pprint import pprint

url = "https://data.alpaca.markets/v2/stocks/AAPL/bars?timeframe=1D&start=2024-06-15&limit=1000&adjustment=raw&feed=sip&sort=asc"

headers = {
    "accept": "application/json",
    "APCA-API-KEY-ID": "PKPUP50BSE5HXH56A1G8",
    "APCA-API-SECRET-KEY": "Fre2uD7RGUiYWiik0CDnfzLs8YDV1ydnqxcGE0X2",
}

response = requests.get(url, headers=headers)

pprint(response.json()["bars"][-2:])
