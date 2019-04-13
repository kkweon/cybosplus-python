from flask import Blueprint, jsonify
from flask_restful import Api, Resource

from API.main import CybosPlus

portfolio_blueprint = Blueprint("portfolio", __name__)
api = Api(portfolio_blueprint)


class Portfolio(Resource):
    def get(self):
        account_numbers = CybosPlus.get_account_number() # tuple
        if len(account_numbers) > 1:
            print("Warning: you got multiple accounts!")
            print("we selected the first account for you...")
            print("account_numbers:", account_numbers)
        account_number = account_numbers[0]
        stocks = CybosPlus.get_account_portfolio(account_number)
        if stocks == -1:
            # Holding no stock!
            # You get into this situation when you are holding only cash.
            stocks = dict() # Just create an empty dict.
        acc_bal = CybosPlus.get_account_balance(account_number)
        stocks["account_balance"] = acc_bal
        stocks["account_number"] = account_number

        return jsonify(stocks)


api.add_resource(Portfolio, "/")
