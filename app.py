# -*- encoding: utf-8 -*-
import sys

from flask import Flask
from flask_restful import Api, Resource
from API.main import CybosPlus

app = Flask(__name__)
api = Api(app)

CybosPlus.initialize()
AccNo = CybosPlus.get_account_number()[0]


class Portfolio(Resource):
    def get(self):
        stocks = CybosPlus.get_account_portfolio(AccNo)
        acc_bal = CybosPlus.get_account_balance(AccNo)
        stocks["account_balance"] = acc_bal
        return stocks


api.add_resource(Portfolio, "/portfolio")

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    app.run(host="0.0.0.0", port=80)
