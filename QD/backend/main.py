# fastapienv\Scripts\activate.bat
# cd QD\backend
# uvicorn main:app --reload
# run this to create the databae
from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path
from starlette import status

import models
from models import Todos
from database import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import yfinance as yf
from pprint import pprint
import requests
import numpy as np

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

###############################
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
###########################


def get_data(ticker):

    # date
    current_date = datetime.now()
    five_days_before = current_date - timedelta(days=5)
    formatted_date = five_days_before.strftime("%Y-%m-%d")

    # alpaca
    url = f"https://data.alpaca.markets/v2/stocks/{ticker}/bars?timeframe=1D&start={formatted_date}&limit=1000&adjustment=raw&feed=sip&sort=asc"
    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": "PKPUP50BSE5HXH56A1G8",
        "APCA-API-SECRET-KEY": "Fre2uD7RGUiYWiik0CDnfzLs8YDV1ydnqxcGE0X2",
    }

    response = requests.get(url, headers=headers)
    latest_two_bars = response.json()["bars"][-2:]
    price1 = latest_two_bars[0]["c"]
    price2 = latest_two_bars[1]["c"]
    current_price = "$" + str(price2)
    pct_change = str(np.round((price2 - price1) / price1 * 100, 2)) + "%"
    up = np.round((price2 - price1) / price1 * 100, 2) >= 0
    # print("Current Price:", current_price)
    # print("pct change:", pct_change)
    return current_price, pct_change, up


def get_watchlist():

    url = "https://paper-api.alpaca.markets/v2/watchlists:by_name?name=my_watchlist"

    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": "PKPUP50BSE5HXH56A1G8",
        "APCA-API-SECRET-KEY": "Fre2uD7RGUiYWiik0CDnfzLs8YDV1ydnqxcGE0X2",
    }

    response = requests.get(url, headers=headers)

    stock_list = [item["symbol"] for item in response.json()["assets"]]
    return stock_list


class StockData(BaseModel):

    companyName: str
    ticker: str
    priceChange: str
    stockPrice: str
    panelColor: str
    priceChangeColor: str
    img: str


################################################################
# GET


@app.get("/data/getall", status_code=status.HTTP_200_OK)
async def all_stocks():
    watchlist = get_watchlist()
    stock_info_list = []

    for idx, ticker in enumerate(watchlist):
        stock_data = StockData(
            companyName="",
            ticker="",
            priceChange="",
            stockPrice="",
            panelColor="",
            priceChangeColor="",
            img="",
        )

        color_list = ["#b6dedc", "#e1ccdb", "#edb4bd", "#ffe5a5"]
        selected_color = color_list[idx % 4]

        current_price, pct_change, up = get_data(ticker)
        stock_data.companyName = yf.Ticker(ticker).info["longName"]
        stock_data.ticker = ticker
        stock_data.stockPrice = current_price
        stock_data.priceChange = pct_change
        stock_data.panelColor = selected_color
        stock_data.priceChangeColor = "#77b900" if up else "#ff2f2f"
        stock_data.img = f"https://raw.githubusercontent.com/davidepalazzo/ticker-logos/main/ticker_icons/{ticker}.png"
        stock_info_list.append(stock_data)
    return stock_info_list


@app.get("/data/{ticker}", status_code=status.HTTP_200_OK)
async def one_stock(ticker: str):
    stock_data = StockData(
        companyName="",
        ticker="",
        priceChange="",
        stockPrice="",
        panelColor="",
        priceChangeColor="",
        img="",
    )

    color_list = ["#b6dedc", "#e1ccdb", "#edb4bd", "#ffe5a5"]
    random_color = color_list[np.random.randint(0, 4)]

    current_price, pct_change, up = get_data(ticker)
    stock_data.companyName = yf.Ticker(ticker).info["longName"]
    stock_data.ticker = ticker
    stock_data.stockPrice = current_price
    stock_data.priceChange = pct_change
    stock_data.panelColor = random_color
    stock_data.priceChangeColor = "#77b900" if up else "#ff2f2f"
    stock_data.img = f"https://raw.githubusercontent.com/davidepalazzo/ticker-logos/main/ticker_icons/{ticker}.png"
    return stock_data
    # return {"current_price": current_price, "pct_change": pct_change}
    # return ticker


# @app.get("/acc", status_code=status.HTTP_200_OK)


"""
@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)  # path parameter
# status_code=status.HTTP_200_OK is optional, but to be explicit
async def read_todo(
     todo_id: int = Path(gt=0)
):  # validation. id must be greater than 0

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    # .first(): to save time. We know there is only one row with this id
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


################################################################
# POST
@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.dict())

    db.add(todo_model)  # getting ready
    db.commit()  # actually adding to the database


################################################################
# PUT
@app.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)
):
    # (db: db_dependency, todo_id: int = Path(gt=0), todo_request: TodoRequest)
    # causes an error because todo_request has to come befor the path parameter

    # get the todo with the id
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.completed = todo_request.completed

    db.add(todo_model)
    db.commit()


################################################################
# DELETE
@app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):

    # get the todo with the id
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
    """
