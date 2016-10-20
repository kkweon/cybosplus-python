from flask import Blueprint, jsonify
from flask_restful import Api, Resource

from API.main import CybosPlus

portfolio_blueprint = Blueprint("portfolio", __name__)
api = Api(portfolio_blueprint)


class Portfolio(Resource):
    def get(self):
        account_number = CybosPlus.get_account_number()[0]
        stocks = CybosPlus.get_account_portfolio(account_number)
        acc_bal = CybosPlus.get_account_balance(account_number)
        stocks["account_balance"] = acc_bal
        stocks["account_number"] = account_number

        return jsonify(stocks)


api.add_resource(Portfolio, "/")
