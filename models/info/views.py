from flask import Blueprint, jsonify
from flask_restful import Resource, Api

from API.main import CybosPlus

info_blueprint = Blueprint('info', __name__)
api = Api(info_blueprint)


class InfoView(Resource):
    def get(self):
        data = dict()
        data['connected'] = CybosPlus.is_connected()
        data['order_limit'] = CybosPlus.get_limit_remain_count(0)
        data['view_limit'] = CybosPlus.get_limit_remain_count(1)
        data['refresh_time'] = CybosPlus.get_limit_remain_time()
        data['market_open'] = CybosPlus.get_market_start_time()
        data['market_close'] = CybosPlus.get_market_close_time()

        return jsonify(data)


api.add_resource(InfoView, "/")
