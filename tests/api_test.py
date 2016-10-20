# encoding: utf-8
import json

import requests


def test_buy_order():
    url = "http://localhost/stock/buy"
    stock1 = {
        "name": "naver",
        "price": 10
    }
    stock2 = {
        "name": "daum",
        "price": 1000
    }
    order_stock_list = [stock1, stock2]
    js = json.dumps(order_stock_list)
    print js
    req = requests.post(url, json=json.dumps(order_stock_list))
    print req.text


def retriev_multiple_stock_info():
    url = "http://localhost/stock/info"
    stock1 = {
        "stock_code": "A047810"
    }
    stock2 = {
        "stock_code": "A035420"
    }
    data = [stock1, stock2]
    js = json.dumps(data)
    req = requests.post(url, json=js)
    print req.text


if __name__ == "__main__":
    retriev_multiple_stock_info()
