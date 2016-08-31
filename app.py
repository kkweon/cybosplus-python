# -*- encoding: utf-8 -*-
import sys

from flask import Flask
from flask import make_response
from flask.templating import render_template
from flask_restful import Api, Resource
from API.main import CybosPlus
import json

app = Flask(__name__)
api = Api(app)

CybosPlus.initialize()
AccNo = CybosPlus.get_account_number()[0]


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
        stocks = CybosPlus.get_account_portfolio(AccNo)
        acc_bal = CybosPlus.get_account_balance(AccNo)
        stocks["account_balance"] = acc_bal

        return make_response(json.dumps(stocks, ensure_ascii=False, indent=4))


class Stock(Resource):
    def get(self, stock_code):
        data = CybosPlus.get_10_latest_quotes(stock_code)
        data = json.dumps(data, ensure_ascii=False, indent=4)
        return make_response(data)

    def post(self):
        pass

    def delete(self):
        pass


@app.route('/')
def home():
    return render_template('index.html')


api.add_resource(Portfolio, "/portfolio/")
api.add_resource(Stock, "/stock/<string:stock_code>")
api.add_resource(BasicInfo, "/info/")

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    app.run(host="0.0.0.0", port=80)
