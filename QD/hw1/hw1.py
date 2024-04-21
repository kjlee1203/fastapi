# fastapienv\Scripts\activate.bat
# deactivate
# uvicorn QD.hw1.hw1:app --reload

from fastapi import Body, FastAPI
import json
from datetime import datetime

app = FastAPI()

# load data from text file
file = open("QD/hw1/data/data_all.txt", "r")
DATA = json.load(file)


# get tickers
@app.get("/api/v1/tickers")
async def get_tickers():
    # make a set so that we don't have duplicates
    tickers = {item["ticker"] for item in DATA}
    return [{"ticker": ticker} for ticker in tickers]


# current price
@app.get("/api/v1/{ticker}/price")
async def get_newest_price(ticker: str):
    newest_date = datetime(1900, 1, 1)
    for item in DATA:
        if (
            item["ticker"].casefold() == ticker.casefold()
            or item["ticker"][4:].casefold() == ticker.casefold()
        ):
            date = datetime.strptime(item["date"], "%Y-%m-%d")
            if date > newest_date:
                newest_date = date
                price = item["close"]
                ticker_to_rtn = item["ticker"][4:]
    if newest_date != datetime(1900, 1, 1):
        return {"currency": "KRW", "ticker": ticker_to_rtn, "price": price}
    else:
        return {"error": "ticker not found"}


# ohlcv data for a specific date
@app.get("/api/v1/{ticker}/ohlcv/{date}")
async def get_ohlcv_specific_date(ticker: str, date: str):
    for item in DATA:
        if (
            item["ticker"].casefold() == ticker.casefold()
            or item["ticker"][4:].casefold() == ticker.casefold()
        ):
            if item["date"] == date:
                return {
                    "date": item["date"],
                    "ticker": item["ticker"][4:],
                    "open": item["open"],
                    "high": item["high"],
                    "low": item["low"],
                    "close": item["close"],
                    "volume": item["volume"],
                }
    return {"error": "ticker or date not found"}


# ohlcv data for a given period using query
@app.get("/api/v1/{ticker}/ohlcv/")
async def get_ohlcv_period(ticker: str, start_date: str, end_date: str):
    ohlcv_data = []
    for item in DATA:
        if (
            item["ticker"].casefold() == ticker.casefold()
            or item["ticker"][4:].casefold() == ticker.casefold()
        ):
            date = datetime.strptime(item["date"], "%Y-%m-%d")
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            if start <= date <= end:
                ohlcv_data.append(
                    {
                        "date": item["date"],
                        "ticker": item["ticker"][4:],
                        "open": item["open"],
                        "high": item["high"],
                        "low": item["low"],
                        "close": item["close"],
                        "volume": item["volume"],
                    }
                )
    if len(ohlcv_data) == 0:
        return {"error": "ticker or date not found"}

    # sort by the ascending order of date
    sorted_data = sorted(ohlcv_data, key=lambda x: x["date"])
    return sorted_data


file.close()
