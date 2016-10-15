# -*- encoding: utf-8 -*-
import json

from flask import Flask
from flask import make_response
from flask import request
from flask.templating import render_template
from flask_restful import Api, Resource

from API.main import CybosPlus

app = Flask(__name__)
api = Api(app)



class BasicInfo(Resource):
    def get(self):
        data = {}
        data['connected'] = CybosPlus.is_connected()
        data['order_limit'] = CybosPlus.get_limit_remain_count(0)
        data['view_limit'] = CybosPlus.get_limit_remain_count(1)
        data['refresh_time'] = CybosPlus.get_limit_remain_time()
        data['market_open'] = CybosPlus.get_market_start_time()
        data['market_close'] = CybosPlus.get_market_close_time()
        data = json.dumps(data, ensure_ascii=False, indent=4)
        return make_response(data)

class Portfolio(Resource):
    def get(self):
        stocks = CybosPlus.get_account_portfolio(account_number)
        acc_bal = CybosPlus.get_account_balance(account_number)
        stocks["account_balance"] = acc_bal

        return make_response(json.dumps(stocks, ensure_ascii=False, indent=4))


class Stock(Resource):
    def get(self, stock_code):
        data = CybosPlus.get_10_latest_quotes(stock_code)
        data = json.dumps(data, ensure_ascii=False, indent=4)
        return make_response(data)

    def post(self, stock_code, buy_or_sell):
        amount = request.form['amount']
        if buy_or_sell == "buy":
            return make_response("{}를 {}개 구매함".format(stock_code, amount))
        elif buy_or_sell == "sell":
            return make_response("{}를 {}개 판매함".format(stock_code, amount))




@app.route('/')
def home():
    return render_template('index.html')

api.add_resource(Portfolio, "/portfolio/")
api.add_resource(Stock, "/stock/<string:stock_code>", "/stock/<string:stock_code>/<string:buy_or_sell>")
api.add_resource(BasicInfo, "/info/")

if __name__ == "__main__":
    CybosPlus.initialize(password="0302")
    account_number = CybosPlus.get_account_number()[0]
    app.run(host="0.0.0.0", port=80)
