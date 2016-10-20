# encoding: utf-8

from flask import Blueprint, jsonify
from flask import request
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


class MultipleStocks(Resource):
    def post(self):
        json_data = request.get_json()
        stock_list = []
        for stock in json_data:
            stock_list.append(stock['stock_code'])
        result = CybosPlus.get_many_info(stock_list)
        return jsonify(result)


class BuyOrder(Resource):
    def post(self):
        data = request.get_json()
        """
        data = [
            stock1,
            stock2,
            ...
        ]

        stock1 = {
            stock_code: ???,
            order_type: ???, // 2=buy or 1=sell // Following the enum_list
            order_price: ???,
            amount: ???,
        }

        """
        account_number = CybosPlus.get_account_number()[0]
        result = list()
        print data
        for order_data in data:
            if order_data['order_type'] == 2:
                one_result = CybosPlus.buy_order(account_number, order_data['stock_code'], order_data['amount'],
                                                 order_data.get('price', 0))
            elif order_data['order_type'] == 1:
                one_result = CybosPlus.sell_order(account_number, order_data['stock_code'], order_data['amount'],
                                                  order_data.get('price', 0))
            result.append(one_result)
        return jsonify(result)


api.add_resource(BuyOrder, '/buy')
api.add_resource(MultipleStocks, '/info')
api.add_resource(IndividualStock, "/info/<string:stock_code>")
