# encoding: utf-8
from flask import Blueprint, jsonify
from flask_restful import Api, Resource

from API.main import CybosPlus

stock_blueprint = Blueprint("stocks", __name__)
api = Api(stock_blueprint)


class IndividualStock(Resource):
    def get(self, stock_code):
        data = CybosPlus.get_quote_by_count(stock_code)

        return jsonify(data)

        # def post(self, stock_code, buy_or_sell):
        #     amount = request.form['amount']
        #     if buy_or_sell == "buy":
        #         return make_response("{}를 {}개 구매함".format(stock_code, amount))
        #     elif buy_or_sell == "sell":
        #         return make_response("{}를 {}개 판매함".format(stock_code, amount))


# class MultipleStocks(Resource):
#     def get(self):
#         stock_list = request.form['']

api.add_resource(IndividualStock, "/<stock_code>")
